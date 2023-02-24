# MCS 275 Spring 2023 Lecture 18

import trees


class IntegerSet:
    "A mutable set of distinct integers (using BST)"

    def __init__(self, values=None):
        """
        Initialize an empty set of integers.  If given, add items from iterable `values`
        to it.
        """
        self.T = trees.BST()
        if values != None:
            for x in values:
                self.add(x)

    def add(self, x):
        "Add the integer `x` to this set"
        node = self.T.search(x)
        if node == None:
            # x is not already in the tree, so we insert it
            self.T.insert(x)

    def __contains__(self, x):
        "Return boolean according to whether or not `x` is in this set"
        node = self.T.search(x)
        return node != None  # True if found, False if not found

    def __str__(self):
        "Human-readable string representation"
        return "{}({})".format(self.__class__.__name__, self.aslist())

    def __repr__(self):
        "Unambiguous string representation"
        return "{}({})".format(self.__class__.__name__, repr(self.aslist()))

    def aslist(self):
        "List of values in this set"
        return self.T.inorder()


class IntegerSetUL(IntegerSet):
    "A mutable set of distinct integers (using unsorted list as backing data structure)"

    def __init__(self, values=None):
        """
        Initialize an empty set of integers.  If given, add items from iterable `values`
        to it.
        """
        self.L = []
        if values != None:
            for x in values:
                self.add(x)

    def add(self, x):
        "Add the integer `x` to this set"
        if x not in self.L:
            self.L.append(x)

    def aslist(self):
        return self.L[:]

    def __contains__(self, x):
        "Return boolean according to whether or not `x` is in this set"
        return x in self.L
