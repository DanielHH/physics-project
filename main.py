
# Import non-standard modules.
import pygame
import sys
import math
import itertools
from Body import Body
from pygame.locals import *
from Rocket import Rocket
import random

width, height = 1280, 720
bodys = {}
x_offset = 0
y_offset = 0
center = ""
monitor = ""
distanceMoon = 0
gamePaused = False
gameOver = False
win = False
isObjective = False
b1 = ""
b1_2 = ""
b1_3 = ""
b1_4 = ""
b2 = ""
b3 = ""
b4 = ""

def update(dt):
    global gamePaused, isObjective
    """
    Update game. Called once per frame.
    dt is the amount of time passed since last frame.
    If you want to have constant apparent movement no matter your framerate,
    what you can do is something like

    x += v * dt

    and this will scale your velocity based on time. Extend as necessary."""
    # Go through events that are passed to the script by the window.
    for event in pygame.event.get():
        # We need to handle these events. Initially the only one you'll want to care
        # about is the QUIT event, because if you don't handle it, your game will crash
        # whenever someone tries to exit.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if b1.collidepoint(pos):
                isObjective = False
                elasticTest()
                restart()
            if b1_2.collidepoint(pos):
                isObjective = False
                elasticTestWithAngle()
                restart()
            if b1_3.collidepoint(pos):
                isObjective = False
                unElasticTest()
                restart()
            if b1_4.collidepoint(pos):
                isObjective = False
                unElasticTestWithAngle()
                restart()

            if b2.collidepoint(pos):
                gravityTest()
                restart()
            if b3.collidepoint(pos):
                sunSystem()
                restart()
            if b4.collidepoint(pos):
                rockyroad()
                restart()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                gamePaused = not gamePaused
        if event.type == QUIT:
            pygame.quit()  # Opposite of pygame.init
            sys.exit()  # Not including this line crashes the script on Windows. Possibly
            # on other operating systems too, but I don't know for sure.
            # Handle other events as you wish.
    if not gamePaused:
        keys = pygame.key.get_pressed()
        time = dt*0.01
        if "rocket" in bodys:
            if keys[K_LEFT]:
                bodys["rocket"].x_vel -= 1 * time
            if keys[K_RIGHT]:
                bodys["rocket"].x_vel += 1 * time
            if keys[K_DOWN]:
                bodys["rocket"].y_vel += 1 * time
            if keys[K_UP]:
                bodys["rocket"].y_vel -= 1 * time

        combinations = itertools.combinations(bodys, 2)
        for c in combinations:
            if c[0] in bodys and c[1] in bodys:
                gravitation(bodys[c[0]], bodys[c[1]])
                if isCollison(bodys[c[0]], bodys[c[1]]):
                    collison(bodys[c[0]], bodys[c[1]])
        for b in bodys:
            velocityToPos(bodys[b], dt)
    if isObjective:
        objective()


def restart():
    global gamePaused
    global win
    global gameOver
    #run gamemode function here:
    gamePaused = False
    win = False
    gameOver = False

def objective():
    global gamePaused
    global win
    global gameOver
    global distanceMoon
    if "moon" in bodys:
        b1 = bodys["moon"]
        b2 = bodys["earth"]
        distanceMoon = math.fabs(math.hypot(b1.x_pos - b2.x_pos, b1.y_pos - b2.y_pos))
        if distanceMoon > 1000:
            win = True
    else:
        gameOver = True
        gamePaused = True

""" Game - Steal the Moon """
def sunSystem():
    global isObjective
    global center
    global monitor
    isObjective = True
    bodys.clear()
    center = "sun"
    monitor = ""
    rocket = Rocket("rocket", 100, 100, 0, 0, 5, 10, (100, 0, 100), True)
    bodys[rocket.name] = rocket
    addBody("earth", 500, 450, 0, -10, 30, 100000, (50, 100, 100), False)
    addBody("moon", 445, 500, 1, -7, 10, 10, (100, 0, 0), True)
    addBody("sun", 750, 450, 0, 0, 70, 4000000, (100, 100, 0), False)

""" Game - Gravity """
def gravityTest():
    global isObjective
    global center
    global monitor
    isObjective = False
    bodys.clear()
    monitor = ""
    center = "center"
    addBody("center", x_offset, y_offset, 0, 0, 40, 2000000, (100, 100, 0), False)

    for i in range(100):
        r1 = random.randint(0, 100)
        r2 = random.randint(0, 100)
        r3 = random.randint(0, 100)
        x = random.randint(0, 1080)
        y = random.randint(0, 720)
        r = random.randint(1, 10)
        addBody(str(i), x, y, 0, 0, r, 3, (r1, r2, r3), True)

""" Game - Inelastic collision """
def unElasticTest():
    global monitor, center
    bodys.clear()
    monitor = "2"
    center = ""
    addBody("1", 0, 450, 4, 0, 60, 1000, (50, 100, 100), False)
    addBody("2", 1280, 450, -4, 0, 60, 1000, (50, 100, 100), False)

""" Game - Inelastic collision with angle """
def unElasticTestWithAngle():
    global monitor, center
    bodys.clear()
    monitor = "2"
    center = ""
    addBody("1", 620, 0, 0, 4, 60, 1000, (50, 100, 100), False)
    addBody("2", 1280, 550, -4, 0, 60, 1000, (50, 100, 100), False)

""" Game - elastic collision """
def elasticTest():
    global monitor, center
    bodys.clear()
    monitor = "2"
    center = ""
    addBody("1", 0, 450, 4, 0, 60, 1000, (100, 0, 0), True)
    addBody("2", 1280, 450, -4, 0, 60, 1000, (0, 100, 0), True)

""" Game - elastic collision with angle """
def elasticTestWithAngle():
    global monitor, center
    bodys.clear()
    monitor = "2"
    center = ""
    addBody("1", 640, 0, 0, 4, 60, 1000, (100, 0, 0), True)
    addBody("2", 1280, 550, -4, 0, 60, 1000, (0, 100, 0), True)

""" Game - A bunch of randomly placed planets with random mass and stuff """
def bigBang():
    global monitor
    global center
    global isObjective
    isObjective = False
    bodys.clear()
    rocket = Rocket("rocket", width/2, height/2, 0, 0, 10, 10, (100, 100, 100), True)
    bodys[rocket.name] = rocket
    monitor = "rocket"
    center = "rocket"
    for i in range(120):
        r1 = random.randint(0, 100)
        r2 = random.randint(0, 100)
        r3 = random.randint(0, 100)
        x = random.randint(0, 1080)
        y = random.randint(0, 720)
        p = random.randint(0, 1)
        x_vel = random.randint(0, 10)
        y_vel = random.randint(0, 20)
        r = random.randint(1, 30)
        m = random.randint(1, 100)
        addBody(str(i), x, y, x_vel, y_vel, r, m, (r1, r2, r3), True)

""" Game - A rocket can push a bunch of smaller objects placed in a line """
def rockyroad():
    global monitor
    global center
    global isObjective
    isObjective = False
    center = ""
    bodys.clear()
    rocket = Rocket("rocket", 100, 100, 0, 0, 10, 100, (100, 100, 100), True)
    bodys[rocket.name] = rocket
    monitor = "rocket"
    road = 0
    for i in range(120):
        r1 = random.randint(0, 100)
        r2 = random.randint(0, 100)
        r3 = random.randint(0, 100)
        y = height/2
        p = random.randint(0, 1)
        x_vel = random.randint(0, 10)
        y_vel = random.randint(0, 20)
        r = random.randint(1, 10)
        x = road + r
        m = random.randint(1, 100)
        addBody(str(i), x, y, 0, 0, r, m, (r1, r2, r3), True)
        road += (r*2) +1

def drawTest():
    global monitor
    global center
    bodys.clear()
    rocket = Rocket("rocket", width + 100, height + 100, 0, 0, 10, 10, (100, 100, 100), True)
    bodys[rocket.name] = rocket
    monitor = "rocket"
    center = "rocket"
    addBody("2", width, height, 0, 0, 60, 1000, (50, 100, 100), False)
    addBody("2", width- 60, height- 60, 0, 0, 60, 1000, (50, 100, 100), False)

def addBody(name, x_pos, y_pos, x_vel, y_vel, r, m, c, p):
    body = Body(name, x_pos, y_pos, x_vel, y_vel, r, m, c, p)
    bodys[body.name] = body

def velocityToPos(b, dt):

    b.x_pos += (b.x_vel * dt * 0.01)
    b.y_pos += (b.y_vel * dt * 0.01)

def isCollison(b1, b2):
    return b1.r+b2.r > distance(b1, b2)

def collison(b1, b2):
    global gameOver
    global gamePaused
    global center
    global monitor
    if b1.p and b2.p:
        d = (b1.r + b2.r) - distance(b1, b2)
        theta = math.atan2(b1.x_pos - b2.x_pos, b1.y_pos - b2.y_pos)
        normal = get_vector((b1.x_pos,b1.y_pos), (b2.x_pos,  b2.y_pos))
        dot_b1 = dot_product((b1.x_vel,b1.y_vel), normal)
        dot_b2 = dot_product((b2.x_vel,b2.y_vel), normal)
        p = float((2.0 * (dot_b1-dot_b2)) / (b1.m + b2.m))
        b1.x_pos += d * math.sin(theta) / 2
        b2.x_pos -= d * math.sin(theta) / 2
        b1.y_pos += d * math.cos(theta) / 2
        b2.y_pos -= d * math.cos(theta) / 2

        new_b2_x_vel = b2.x_vel + (p * b2.m * normal[0])
        new_b2_y_vel = b2.y_vel + (p * b2.m * normal[1])
        new_b1_x_vel = b1.x_vel - (p * b1.m * normal[0])
        new_b1_y_vel = b1.y_vel - (p * b1.m * normal[1])
        b2.x_vel = new_b2_x_vel
        b2.y_vel = new_b2_y_vel
        b1.x_vel = new_b1_x_vel
        b1.y_vel = new_b1_y_vel
        #b2.x_vel = (b1.m * b1.x_vel) / b2.m
        #b2.y_vel = (b1.m * b1.y_vel) / b2.m
        #b1.x_vel = -((b2.m * b2.x_vel) / b1.m)
        #b1.y_vel = -((b2.m * b2.y_vel) / b1.m)
    else:
        if b1.name == "rocket" or b2.name == "rocket":
            gameOver = True
            gamePaused = True
        else:
            x_vel = ((b1.m * b1.x_vel) + (b2.m * b2.x_vel)) / (b2.m+b1.m)
            y_vel = ((b1.m * b1.y_vel) + (b2.m * b2.y_vel)) / (b2.m + b1.m)
            r = math.sqrt(((math.pi * math.pow(b1.r, 2)) + (math.pi * math.pow(b2.r, 2)))/math.pi)
            d = distance(b1,b2)
            if d == 0:
                d = 1
            x_pos = b1.x_pos + ((1-(b1.r/d)) * (b2.x_pos - b1.x_pos))
            y_pos = b1.y_pos + ((1-(b1.r/d)) * (b2.y_pos - b1.y_pos))
            m = b1.m+b2.m
            c = (b1.c[0], b2.c[1], b1.c[2])
            p = False
            new_body = Body(b1.name+b2.name,x_pos, y_pos, x_vel, y_vel, r, m, c, p)
            bodys[new_body.name] = new_body
            if b1.name == center or b2.name == center:
               center = b1.name+b2.name
            if b1.name == monitor or b2.name == monitor:
                monitor = b1.name+b2.name
            del bodys[b1.name]
            del bodys[b2.name]

def get_vector(p1, p2):
    dis = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    direction = (p2[0] - p1[0], p2[1] - p1[1])
    normalized = (direction[0] / dis, direction[1] / dis)
    return normalized

def dot_product(v1, v2):
    return sum([i*j for (i, j) in zip(v1, v2)])

def distance(b1, b2):
    return math.hypot(math.fabs(b1.x_pos - b2.x_pos), math.fabs(b1.y_pos - b2.y_pos))

def gravitation(b1, b2):
    g = 0.001
    r = distance(b1, b2)
    if r == 0:
        r = 0.1
    theta = math.atan2((b1.x_pos - b2.x_pos), b1.y_pos - b2.y_pos)
    f = g*b1.m*b2.m/(r**2)
    b1.x_vel -= f/b1.m * math.sin(theta)
    b1.y_vel -= f/b1.m * math.cos(theta)
    b2.x_vel += f/b2.m * math.sin(theta)
    b2.y_vel += f/b2.m * math.cos(theta)


def draw(screen):
    """
    Draw things to the window. Called once per frame.
    """
    screen.fill((0, 0, 0))
    x_c = x_offset
    y_c = y_offset
    if center:
        x_c = int(bodys[center].x_pos)
        y_c = int(bodys[center].y_pos)
        pygame.draw.circle(screen, bodys[center].c, (x_offset, y_offset), int(bodys[center].r), 0)

    for b in bodys:
        if b != center:
            if (width - (bodys[b].x_pos - x_c + x_offset - bodys[b].r)) >= 0 and \
                    (height - (bodys[b].y_pos - y_c + y_offset - bodys[b].r)) >= 0:

                pygame.draw.circle(screen, bodys[b].c, (int(bodys[b].x_pos - x_c) + x_offset,
                                                        int(bodys[b].y_pos - y_c) + y_offset),
                                   int(bodys[b].r), 0)


    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    if monitor in bodys:
        name = myfont.render("Monitor of: " + str(bodys[monitor].name), False, (100, 100, 100))
        screen.blit(name, (10, 10))
        x_vel = myfont.render("Velocity in X: " + str(bodys[monitor].x_vel), False, (100, 100, 100))
        y_vel = myfont.render("Velocity in Y: " + str(bodys[monitor].y_vel), False, (100, 100, 100))
        screen.blit(x_vel, (10, 40))
        screen.blit(y_vel, (10, 70))
        x_pos = myfont.render("Pos in X: " + str(bodys[monitor].x_pos), False, (100, 100, 100))
        y_pos = myfont.render("Pos in Y: " + str(bodys[monitor].y_pos), False, (100, 100, 100))
        screen.blit(x_pos, (10, 100))
        screen.blit(y_pos, (10, 130))

    if isObjective:
        moon = myfont.render("Moons distance from earth: " + str(distanceMoon), False, (100, 100, 100))
        screen.blit(moon, (width - 400, 20))
    if gamePaused:
        drawPauseMenu(screen, myfont)
    if win:
        pausedgame = myfont.render("You win the moon is now lose in the universe!", False, (100, 100, 100))
        screen.blit(pausedgame, (x_offset - 300, y_offset - 200))
    if gameOver:
        pausedgame = myfont.render("You lose! Chose new game mode", False, (100, 100, 100))
        screen.blit(pausedgame, (x_offset - 300, y_offset - 200))
    # Flip the display so that the things we drew actually show up.
    pygame.display.flip()

def drawPauseMenu(screen, font):
    global b1, b1_2, b1_3, b1_4, b2, b3, b4


    b1 = pygame.draw.rect(screen, (100, 100, 100), ((width/2)-100, (height/2) -100, 50, 50))

    b1_2 = pygame.draw.rect(screen, (90, 90, 90), ((width / 2) - 50, (height / 2) - 100, 50, 50))
    b1_3 = pygame.draw.rect(screen, (100, 100, 100), ((width / 2) , (height / 2) - 100, 50, 50))
    b1_4 = pygame.draw.rect(screen, (90, 90, 90), ((width / 2) + 50, (height / 2) - 100, 50, 50))
    b1_text = font.render("Collisions", False, (0, 0, 0))
    screen.blit(b1_text, ((width / 2) - 100 + 20, (height / 2) - 100 + 20))

    b2 = pygame.draw.rect(screen, (75, 75, 75), ((width/2) - 100, (height/2), 200, 50))
    b2_text = font.render("Gravity", False, (0, 0, 0))
    screen.blit(b2_text, ((width / 2) - 100 + 20, (height / 2) + 20))

    b3 = pygame.draw.rect(screen, (75, 75, 75), ((width / 2) - 100, (height / 2) + 100, 200, 50))
    b3_text = font.render("Steal the moon", False, (0, 0, 0))
    screen.blit(b3_text, ((width / 2) - 100 + 20, (height / 2) + 100 + 20))

    b4 = pygame.draw.rect(screen, (75, 75, 75), ((width / 2) - 100, (height / 2) + 200, 200, 50))
    b4_text = font.render("Random", False, (0, 0, 0))
    screen.blit(b4_text, ((width / 2) - 100 + 20, (height / 2) + 200 + 20))




def runPyGame():
    global x_offset
    global y_offset
    global gamePaused
    # Initialise PyGame.
    pygame.init()
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.


    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 60.0
    fpsClock = pygame.time.Clock()

    # Set up the window.
    width, height = 1280, 720
    x_offset = width/2
    y_offset = height/2
    screen = pygame.display.set_mode((width, height))

    # Set up the name of the game
    name = 'Steal The Moon!'
    pygame.display.set_caption(name)

    # screen is the surface representing the window.
    # PyGame surfaces can be thought of as screen sections that you can draw onto.
    # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.

    gamePaused = True
    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.
    while True:  # Loop forever!
        update(dt)  # You can update/draw here, I've just moved the code for neatness.
        draw(screen)

        dt = fpsClock.tick(fps)

runPyGame()