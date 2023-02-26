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
        if not isinstance(x, int):
            raise ValueError("Only integers supported")
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
        if not isinstance(x, int):
            raise ValueError("Only integers supported")
        if x not in self.L:
            self.L.append(x)

    def aslist(self):
        return self.L[:]

    def __contains__(self, x):
        "Return boolean according to whether or not `x` is in this set"
        return x in self.L


class IntegerSetSL(IntegerSetUL):
    "A mutable set of distinct integers (using sorted list as backing data structure)"

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
        if x in self.L:
            return
        if not isinstance(x, int):
            raise ValueError("Only integers supported")
        self.L.append(x)
        self.L.sort()  # needlessly slow; could use bisection to find place to insert

    def __contains__(self, x):
        # Bisection search; look at middle value, decide whether
        # the desired element would appear earlier or later
        if not self.L:
            return
        low = 0
        high = len(self.L) - 1
        while low < high:
            mid = (low + high) // 2
            y = self.L[mid]
            if x == y:
                return True
            elif x < y:
                high = mid - 1
            else:
                low = mid + 1
        return x == self.L[low]


if __name__ == "__main__":
    import random
    import time

    n = 20000
    Linsert = [random.randint(1, 5 * n) for _ in range(n)]
    Lcheck = [random.randint(1, 5 * n) for _ in range(n // 2)] + Linsert[: n // 2]
    random.shuffle(Lcheck)

    implementations = [IntegerSetUL, IntegerSetSL, IntegerSet]

    for cls in implementations:
        print("Testing {} with {} elements:".format(cls.__name__, n))
        t0 = time.time()
        S = cls(Linsert)
        t1 = time.time()
        checks = [x in S for x in Lcheck]
        t2 = time.time()
        print("{:.2f}s insert".format(t1 - t0))
        print("{:.2f}s membership test".format(t2 - t1))
