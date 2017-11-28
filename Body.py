
class Body(object):
    """A Body is a circular planet or a moon in the Space universe. Planets have the following properties:

    Attributes:
        name: a string representing the planet's name
        x_pos: float representing x-position
        y_pos: float representing y-position
        x_vel: float representing x-velocity
        y_vel: float representing y-velocity
        r: float representing the radius of a body.
        m: a float representing the body's weight in kg.
        p: booleans pushable
        """

    def __init__(self, name, x_pos, y_pos, x_vel, y_vel, r, m, c, p):
        """Returns a Body"""
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.r = r
        self.m = m
        self.c = c
        self.p = p
