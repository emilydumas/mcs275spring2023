# MCS 275 Spring 2023 Project 1 Solution
# David Dumas

"Classes representing shuttle autopilot strategies"

# ----------------------------------------------------------------------
#          THIS BASE CLASS WAS PROVIDED IN THE STARTER PACK
# ----------------------------------------------------------------------


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
        self.capacity = capacity  # max material shuttle can hold
        self.stored = 0  # current amount stored by shuttle
        self.pos = 0  # position, an integer from 0 to 9 inclusive

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
#            THIS IS THE PART STUDENTS WERE ASKED TO WRITE
# ----------------------------------------------------------------------


class BackForthShuttle(Shuttle):
    "Shuttle that goes back and forth on a regular schedule"

    def __init__(self, capacity, supply, dest):
        "Initialize shuttle state machine to handle load/move/unload steps"
        super().__init__(capacity, supply, dest)
        self.handlers = {
            "load": self.load_update,
            "forward": self.forward_update,
            "backward": self.backward_update,
            "unload": self.unload_update,
        }
        self.state = "load"

    def update(self):
        "Advance the simulation one unit of time"
        self.handlers[self.state]()

    # Optional metod
    def __str__(self):
        "Human readable string representation"
        return '{}(pos={},capacity={},stored={},state="{}")'.format(
            self.__class__.__name__,
            self.pos,
            self.capacity,
            self.stored,
            self.state,
        )

    # Optional metod
    def __repr__(self):
        "Unambiguous readable string representation"
        return str(self)

    def load_update(self):
        "Handle one time step in the `load` state"
        assert self.pos == 0  # Enforce policy: load only at 0
        req = self.available_capacity()
        amt = self.supply.remove_material(req)
        self.stored += amt
        self.state = "forward"

    def forward_update(self):
        "Handle one time step in the `forward` state"
        assert self.pos < 9  # Enforce policy: Only step forward when not at end
        self.pos += 1
        if self.pos == 9:
            self.state = "unload"

    def backward_update(self):
        "Handle one time step in the `backward` state"
        assert self.pos > 0  # Enforce policy: Only step back when not at start
        self.pos -= 1
        if self.pos == 0:
            self.state = "load"

    def unload_update(self):
        "Handle one time step in the `unload` state"
        assert self.pos == 9  # Enforce policy: Only unload at end (dest)
        amt = self.dest.add_material(self.stored)
        self.stored -= amt
        self.state = "backward"


# Since `BackForthShuttle` has a state machine and separate methods
# for each state, we can pretty flexibly modify the behavior in a
# subclass just by overriding the state handlers that need to change.
# We do that here so `ActOnOverflowShuttle` can inherit from it.
class ActOnOverflowShuttle(BackForthShuttle):
    "Shuttle that only takes a load when the supply is full"

    def __init__(self, capacity, supply, dest):
        "Initialize shuttle state machine to handle wait/load/move/unload steps"
        super().__init__(capacity, supply, dest)
        self.state = "wait"
        self.handlers = {
            "wait": self.wait_update,  # new state: waiting for overflow
            "forward": self.forward_update,
            "backward": self.backward_update,
            "unload": self.unload_update,
        }

    def wait_update(self):
        "Handle time step in `wait` state"
        # Check for overflow
        if self.supply.is_full():
            # Load material and trigger movement on next step
            amt = self.supply.remove_material(self.available_capacity())
            self.stored += amt
            self.state = "forward"

    def backward_update(self):
        "Handle time step in `backward` state"
        # Same actions as the superclass...
        super().backward_update()
        # ...except we need to adjust the next state
        # to be "wait" instead of "load".  We could
        # have just used the name "load" for the waiting
        # state, but naming states semantically seems
        # best.
        if self.pos == 0:
            self.state = "wait"


# Same story: We can subclass `BackForthShuttle`, only defining
# the methods that need to change.
class ActOnUnderflowShuttle(BackForthShuttle):
    "Shuttle that only takes a load when the dest is empty"

    def __init__(self, capacity, supply, dest):
        "Initialize shuttle state machine to handle wait/load/move/unload steps"
        super().__init__(capacity, supply, dest)
        self.state = "wait"
        self.handlers = {
            "wait": self.wait_update,
            "forward": self.forward_update,
            "backward": self.backward_update,
            "unload": self.unload_update,
        }

    def wait_update(self):
        "Handle time step in `wait` state"
        if self.dest.is_empty():
            req = self.available_capacity()
            amt = self.supply.remove_material(req)
            self.stored += amt

            # Only transition to next state if we actually
            # have some sand on board.
            if self.stored:
                self.state = "forward"

    def backward_update(self):
        "Handle time step in `backward` state"
        # Just like superclass backward_update
        # But with transition to "wait" instead of "unload"
        super().backward_update()
        if self.pos == 0:
            self.state = "wait"
