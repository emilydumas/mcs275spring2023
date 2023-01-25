"""Classes representing robots in a simulation"""
# MCS 275 Spring 2023 David Dumas

import plane
import random


class Bot:
    """Base class for all robots.  Sits in one place forever."""

    symbol = "B"

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


class WanderBot(Bot):
    "Robot that makes a random movement at each time step"
    symbol = "W"
    # Create a CLASS ATTRIBUTE shared by all instances of WanderBot
    steps = [
        plane.Vector2(1, 0),
        plane.Vector2(-1, 0),
        plane.Vector2(0, 1),
        plane.Vector2(0, -1),
    ]

    def update(self):
        "Take a random step"
        # Choose one of these steps at random
        v = random.choice(self.steps)
        # Add v to the position of this robot
        self.move(v)


class FastWanderBot(WanderBot):
    "Robot that makes a random movement (NSEW or diagonal) at each time step"
    symbol = "F"
    steps = [
        plane.Vector2(1, 0),
        plane.Vector2(-1, 0),
        plane.Vector2(0, 1),
        plane.Vector2(0, -1),
        plane.Vector2(1, 1),
        plane.Vector2(1, -1),
        plane.Vector2(-1, 1),
        plane.Vector2(-1, -1),
    ]


class DestructBot(Bot):
    "Robot that sits in one place for a specified amount of time, then deactivates"
    symbol = "D"

    def __init__(self, position, active_time):
        """
        Initialize a DestructBot at position `position` and which will
        remain active for `active_time` time steps
        """
        # Old initialization
        super().__init__(position)
        # New initialization
        self.active_time = active_time  # will stay the same on each update
        self.remaining_time = active_time  # will decrease by 1 each update

        # Note: we don't strictly need to store active_time, as it's only
        # the remaining time that this instance needs to do its work. It's
        # a matter of taste whether to do so.

    def __str__(self):
        "Human-readable string representation"
        return "{}(position={},active_time={},remaining_time={},active={})".format(
            self.__class__.__name__,
            self.position,
            self.active_time,  # <-- we stored it, so it's nice to display it
            self.remaining_time,
            self.active,
        )

    def update(self):
        "Make note of the passage of one unit of time, deactivating if we're out of time"
        if self.remaining_time == 0:
            self.active = False
        else:
            self.remaining_time -= 1
