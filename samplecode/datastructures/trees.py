# MCS 275 Lecture 16
"Binary tree classes"


class Node:
    "Node in a binary tree"

    def __init__(self, key=None, left=None, right=None):
        """
        Initialize a binary tree node with left child `left` and right
        child `right`
        """
        self.key = key  # Any value we want to store at this node
        self.left = left  # Meant to be None or a `Node`
        self.right = right  # Meant to be None or a `Node`

    def __str__(self):
        "Human-readable string representation"
        return "<{}>".format(self.key)

    def __repr__(self):
        "Unambiguous string representation"
        return str(self)

# TODO: How would we implement __eq__ for trees?

# Lecture 17 will add class `BST` here
