
# Import non-standard modules.
import pygame
import math
import itertools
from Body import Body
from pygame.locals import *
from Rocket import Rocket

bodys = {}
gamePaused = False

def update(dt):
    global gamePaused
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
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                bodys["rocket"].x_vel -= 1
            if event.key == K_RIGHT:
                bodys["rocket"].x_vel += 1
            if event.key == K_DOWN:
                bodys["rocket"].y_vel += 1
            if event.key == K_UP:
                bodys["rocket"].y_vel -= 1
            if event.key == K_SPACE:
                restart()
        if event.type == QUIT:
            pygame.quit()  # Opposite of pygame.init
            sys.exit()  # Not including this line crashes the script on Windows. Possibly
            # on other operating systems too, but I don't know for sure.
            # Handle other events as you wish.
    if not gamePaused:
        combinations = itertools.combinations(bodys, 2)
        for c in combinations:
            print c[0], c[1]
            gravitation(bodys[c[0]], bodys[c[1]])
            if isCollison(bodys[c[0]], bodys[c[1]]):
                if bodys[c[0]].p == True and bodys[c[1]].p == True:
                    collison(bodys[c[0]], bodys[c[1]])
                else:
                    if c[0] == "rocket" or c[1] == "rocket":
                        gamePaused = True
                    #todo make function that remove body and give its force to the larger body make else here
        for b in bodys:
            velocityToPos(bodys[b])


def restart():
    global gamePaused
    bodys.clear()
    rocket = Rocket("rocket", 0, 0, 0, 0, 10, 10, (100, 0, 100), True)
    earth = Body("earth", 400, 450, 0, -3, 60, 1000, (50, 100, 100), False)
    moon = Body("moon", 300, 450, 0, -3.7, 20, 30, (100, 0, 0), True)
    sun = Body("sun", 750, 450, 0, 0, 100, 10000, (100, 100, 0), False)
    bodys[earth.name] = earth
    bodys[moon.name] = moon
    bodys[rocket.name] = rocket
    bodys[sun.name] = sun
    gamePaused = False

def velocityToPos(b):

    b.x_pos += b.x_vel
    b.y_pos += b.y_vel

def isCollison(b1, b2):
    return b1.r+b2.r >= distance(b1, b2)

def collison(b1, b2):
    d = (b1.r + b2.r) - distance(b1, b2)
    theta = math.atan2((b1.x_pos - b2.x_pos), b1.y_pos - b2.y_pos)
    b1.x_pos += d*math.cos(theta)/2
    b2.x_pos -= d * math.cos(theta)/2
    b1.y_pos += d * math.sin(theta) / 2
    b2.y_pos -= d * math.sin(theta) / 2

    b2.x_vel = (b1.m * b1.x_vel)/b2.m
    b2.y_vel = (b1.m * b1.y_vel)/b2.m
    b1.x_vel = -((b2.m * b2.x_vel) / b1.m)
    b1.y_vel = -((b2.m * b2.y_vel) / b1.m)

def distance(b1, b2):
    return math.hypot(math.fabs(b1.x_pos - b2.x_pos), math.fabs(b1.y_pos - b2.y_pos))

def gravitation(b1, b2):
    g = 0.001
    r = distance(b1, b2)
    theta = math.atan2((b1.x_pos - b2.x_pos), b1.y_pos - b2.y_pos)
    f = g*b1.m*b2.m/r
    b1.x_vel -= f/b1.m * math.sin(theta)
    b1.y_vel -= f/b1.m * math.cos(theta)
    b2.x_vel += f/b2.m * math.sin(theta)
    b2.y_vel += f/b2.m * math.cos(theta)


def draw(screen):
    """
    Draw things to the window. Called once per frame.
    """

    screen.fill((0, 0, 0))
    for b in bodys:
        pygame.draw.circle(screen, bodys[b].c, (int(bodys[b].x_pos), int(bodys[b].y_pos)), bodys[b].r, 0)

    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    x_vel = myfont.render("Velocity in X: " + str(bodys["rocket"].x_vel), False, (100, 100, 100))
    y_vel = myfont.render("Velocity in Y: " + str(bodys["rocket"].y_vel), False, (100, 100, 100))
    screen.blit(x_vel, (10, 10))
    screen.blit(y_vel, (10, 40))
    x_pos = myfont.render("Pos in X: " + str(bodys["rocket"].x_pos), False, (100, 100, 100))
    y_pos = myfont.render("Pos in Y: " + str(bodys["rocket"].y_pos), False, (100, 100, 100))
    screen.blit(x_pos, (10, 70))
    screen.blit(y_pos, (10, 100))
    # Flip the display so that the things we drew actually show up.
    pygame.display.flip()


def runPyGame():
    # Initialise PyGame.
    pygame.init()
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.


    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 60.0
    fpsClock = pygame.time.Clock()

    # Set up the window.
    width, height = 1500, 700
    screen = pygame.display.set_mode((width, height))

    # Set up the name of the game
    name = 'Steal The Moon!'
    pygame.display.set_caption(name)

    # screen is the surface representing the window.
    # PyGame surfaces can be thought of as screen sections that you can draw onto.
    # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.

    restart()
    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.
    while True:  # Loop forever!
        update(dt)  # You can update/draw here, I've just moved the code for neatness.
        draw(screen)

        dt = fpsClock.tick(fps)

runPyGame()