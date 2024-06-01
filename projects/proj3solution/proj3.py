# MCS 275 Spring 2023 Project 3 Solution
# Emily Dumas
"Partial replacement for Python `dict` build using a binary tree"

class KVNode:
    "Node in a binary tree that stores both key and value"

    def __init__(self, key=None, value=None, left=None, right=None, parent=None):
        """
        Initialize a binary tree node with left child `left` and right
        child `right`
        """
        self.key = key
        self.value = value
        self.left = left  # Meant to be None or a `Node`
        self.right = right  # Meant to be None or a `Node`
        self.parent = parent  # Meant to be None or a `Node`

    def __str__(self):
        "Human-readable string representation"
        return "<{}:{}>".format(repr(self.key), repr(self.value))

    def __repr__(self):
        "Unambiguous string representation"
        return str(self)

    def nodes(self):
        "Returns a list of nodes in this tree using inorder traversal"
        if self.key == None:
            return []  # empty tree is indicated by key None
        nodes_in_left_subtree = []
        if self.left != None:
            nodes_in_left_subtree = self.left.nodes()  # recursion!
        nodes_in_right_subtree = []
        if self.right != None:
            nodes_in_right_subtree = self.right.nodes()
        return nodes_in_left_subtree + [self] + nodes_in_right_subtree

    def keys(self):
        "List of keys (inorder)"
        return [n.key for n in self.nodes()]

    def values(self):
        "List of keys (inorder)"
        return [n.value for n in self.nodes()]

    def items(self):
        "List of keys (inorder)"
        return [(n.key, n.value) for n in self.nodes()]


class KVBST(KVNode):
    "Binary search tree class (with recursive insert, search)"

    def search(self, k, verbose=False):
        """
        Find a node in this tree with key `k` and return it;
        return None if no such node exists.
        """
        if verbose:
            print("At", self, "searching for key", k)
        if self.key == None:
            # Handle empty BST, which never contains anything
            return None
        if k == self.key:
            # This is the right node!  Return it
            if verbose:
                print("Success! Returning this node.")
            return self
        elif k < self.key:
            # The node with key `k` must be in the left subtree
            if self.left == None:
                # Lack of left child means `k` is not present
                if verbose:
                    print("Dead end; there is no node with key", k)
                return None
            else:
                if verbose:
                    print("Descending into left subtree")
                return self.left.search(k, verbose)
        elif self.key < k:
            # The node with key `k` must be in the right subtree
            if self.right == None:
                # Lack of right child means `k` is not present
                if verbose:
                    print("Dead end; there is no node with key", k)
                return None
            else:
                if verbose:
                    print("Descending into right subtree")
                return self.right.search(k, verbose)

    def insert(self, k, v):
        """
        Find a suitable place to add a new node to this BST
        with key `k`, and add it.
        """
        if self.key == None:
            # Empty tree, so just make this node have key `k`
            self.key = k
            self.value = v
            return
        if k <= self.key:
            if self.left == None:
                # `k` belongs to the left, and the left is empty.
                # Create a new node and make it the left child
                node = KVBST(key=k, value=v, parent=self)
                self.left = node
            else:
                # Have the left subtree handle it
                self.left.insert(k, v)
        else:
            if self.right == None:
                # `k` belongs to the right, and the right is empty.
                # Create a new node and make it the right child
                node = KVBST(key=k, value=v, parent=self)
                self.right = node
            else:
                # Have the right subtree handle it
                self.right.insert(k, v)


class Dictionary:
    "`dict` clone with limited functionality, backed by a BST"

    def __init__(self, starting_items=None):
        "Initialize empty dictionary, add `starting_items` if given."
        self.T = KVBST()
        if starting_items is not None:
            for k in starting_items:
                self[k] = starting_items[k]

    def __getitem__(self, k):
        "Retrieve value associated with key `k`"
        node = self.T.search(k)
        if node is None:
            raise KeyError("Not found: " + str(k))
        return node.value

    def __setitem__(self, k, v):
        "Set value associated with key `k` to `v`"
        node = self.T.search(k)
        if node is not None:
            node.value = v
        else:
            self.T.insert(k, v)

    def __str__(self):
        "Human readable"
        return "{}({})".format(
            self.__class__.__name__, repr({k: v for k, v in self.T.items()})
        )

    def __contains__(self, k):
        "Check whether `k` is a key"
        try:
            n = self[k]
            return True
        except KeyError:
            return False

    def __repr__(self):
        "Unambiguous"
        return str(self)

    def __len__(self):
        "Number of keys"
        return len(self.T.nodes())


# ------------------------------------------------------------
#   TESTS
# ------------------------------------------------------------


def test_empty():
    "Create and print empty Dictionary"
    print("Making empty dictionary D")
    D = Dictionary()
    print("D =", D)


def test_nonempty():
    "Create and print nonempty Dictionary"
    print("Making nonempty dictionary D")
    D = Dictionary({481: "CG", 275: "PTFM"})
    print("D =", D)


def test_retrieval_existent():
    "Test retrieval of keys"
    start = {2: "a", 7: "e", 19: "q", 178: "quail"}
    D = Dictionary(start)
    print("Using test dictionary D =", D)
    for k in start:
        print("Testing retrieval of key {}".format(repr(k)))
        print("D[{}] = {}".format(repr(k), repr(D[k])))


def test_retrieval_nonexistent():
    "Test retrieval of nonexistent keys"
    start = {2: "Helium", 3: "Lithium", 92: "Uranium"}
    D = Dictionary(start)
    print("Using test dictionary D =", D)
    for k in [5, 9, 100]:
        print("Testing retrieval of key {}".format(repr(k)))
        success = True
        try:
            D[k]
        except Exception as e:
            print("Exception of type {} was rasied.".format(e.__class__.__name__))
            success = False
        assert success == False


def test_mutation():
    "Test that values associated with keys can be changed"
    print("Making empty Dictionary D")
    D = Dictionary()
    for k, v in [(2, 5), (2, 191457)]:
        D[k] = v
        print("Set D[{}] = {}".format(repr(k), repr(v)))
        x = D[k]
        print("Retrieved D[{}] = {}".format(repr(k), x))
        assert x == v


def test_assign_many():
    "Test adding random keys to a dictionary"
    t0 = time.time()
    D = Dictionary()
    pairs = [
        (random.randrange(1_000_000), random.randrange(1_000_000))
        for _ in range(10_000)
    ]
    print("Adding 10000 key-value pairs")
    for k, v in pairs:
        D[k] = v
    t1 = time.time()
    print("Done (took {:.2f} seconds)".format(t1 - t0))


def printbox(s):
    "Display string s surrounded by a box"
    n = len(s)
    print("\u250c" + "\u2500" * (n + 2) + "\u2510")
    print("\u2502", s, "\u2502")
    print("\u2514" + "\u2500" * (n + 2) + "\u2518")


if __name__ == "__main__":
    # Run the test cases
    import random
    import time

    test_cases = [
        test_empty,
        test_nonempty,
        test_retrieval_existent,
        test_retrieval_nonexistent,
        test_mutation,
        test_assign_many,
    ]
    for f in test_cases:
        printbox("Calling {}".format(f.__name__))
        f()
        print()
