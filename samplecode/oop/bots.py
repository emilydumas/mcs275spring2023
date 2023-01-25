"""Classes representing robots in a simulation"""
# MCS 275 Spring 2023 David Dumas

import plane

# TODO: Add subclasses
# TODO: Class attribute for symbol


class Bot:
    """Base class for all robots.  Sits in one place forever."""

    def __init__(self, position):
        """Setup with initial position `position` (a plane.Point2 instance)"""
        self.active = True
        if not isinstance(position, plane.Point2):
            raise TypeError("Bot position must be a Point2")
        self.position = position

    def move(self, v):
        "Move the position of this Bot by Vector2 `v`"
        self.position = self.position + v

    def __str__(self):
        """Human-readable string representation"""
        return "{}(position={},active={})".format(
            self.__class__.__name__,
            self.position,
            self.active,
        )

    def __repr__(self):
        """Unambiguous string representation"""
        return str(self)

    def update(self):
        """Advance one time step (by doing nothing)"""
