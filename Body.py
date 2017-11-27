
class Body(object):
    """A Body is a circular planet or a moon in the Space universe. Planets have the following properties:

    Attributes:
        name: a string representing the planet's name
        position: floats x- and y-coordinates describing it's posittion in the Space universe.
        velocity: floats x- and y-velocities
        radius: float describing the radius of a body.
        mass: a float representing the body's weight in kg.
        """

    def __init__(self, name, position, velocity, radius, mass):
        """Returns a Body"""
        self.name = name
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.mass = mass

    