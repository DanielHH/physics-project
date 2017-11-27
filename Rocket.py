
class Rocket:
    angle = 0
    thruster_force = 40

    def __init__(self, name, x_pos, y_pos, x_vel, y_vel, r, m, c):
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.r = r
        self.m = m
        self.c = c

