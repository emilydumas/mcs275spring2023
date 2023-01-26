# MCS 275 Spring 2023 Project 1 Starter Pack
# EDIT AND SUBMIT THIS FILE
# Replace this block of comments with the usual header

"Classes representing shuttle autopilot strategies"

# Do not edit this class
class Shuttle:
    "Base class for all shuttle autopilots"

    def __init__(self, capacity, supply, dest):
        """
        Initialize autopilot for shuttle with capacity `capacity`
        using `SupplyCache` object `supply` and `DestinationCache`
        object `dest`.  Starts at position 0.
        """
        self.supply = supply  # Used to interact with supply cache at pos 0
        self.dest = dest  #  Used to interacr with dest. cache at pos 9
        self.capacity = capacity # max material shuttle can hold
        self.stored = 0 # current amount stored by shuttle
        self.pos = 0 # position, an integer from 0 to 9 inclusive

    def available_capacity(self):
        """
        Return how much additional material the shuttle can take
        on right now.
        """
        return self.capacity - self.stored

    def update(self):
        """
        Simulate one minute of time, taking autopilot actions as
        appropriate.  This base class does nothing.  Subclasses
        are supposed to override this method to implement behavior.
        """
        pass


# ----------------------------------------------------------------------
#            ADD YOUR SUBCLASSES OF `Shuttle` BELOW
# ----------------------------------------------------------------------
