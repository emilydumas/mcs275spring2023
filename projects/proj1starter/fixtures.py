# MCS 275 Spring 2023 Project 1 Starter Pack
"Classes representing fixed-position material stores"


class Cache:
    "Base class for anything that stores material"

    def __init__(self, capacity):
        "Initialize an empty material store with given capacity"
        self.capacity = capacity
        self.stored = 0

    def is_full(self):
        "Is this cache at capacity?"
        return self.stored == self.capacity

    def is_empty(self):
        "Is this cache empty?"
        return self.stored == 0

    def add_material(self, amount):
        "Attempt to add `amount` material.  Return amount actually added."
        avail = self.capacity - self.stored
        load = min(amount, avail)
        self.stored += load
        return load

    def remove_material(self, amount):
        "Attempt to remove `amount` material.  Return amount actually removed."
        load = min(amount, self.stored)
        self.stored -= load
        return load

    def __str__(self):
        "Human-readable string representation"
        return "{}(capacity={},stored={})".format(
            self.__class__.__name__, self.capacity, self.stored
        )

    def __repr__(self):
        "Unambiguous string representation"
        return str(self)

    def update(self):
        "Update cache simulation by one minute; does nothing in this base class"
        pass


class SupplyCache(Cache):
    """
    Cache of material that only allows removal through method calls.  Subclasses might add
    material addition in `update()`.
    """

    def add_material(self):
        raise Exception("SupplyCache doesn't allow addition of material")


class DestinationCache(Cache):
    """
    Cache of material that only allows addition through method calls.  Subclasses might add
    material removals in `update()`.
    """

    def remove_material(self):
        raise Exception("DestinationCache doesn't allow addition of material")
