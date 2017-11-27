
class Rocket:

    x_pos = 0
    y_pos = 0
    x_vel = 0
    y_vel = 0
    m = 0
    r = 0
    angle = 0
    thruster_force = 40

    def __init__(self, x_pos, y_pos, m, r):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.m = m
        self.r = r


