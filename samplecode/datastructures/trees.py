# MCS 275 Lectures 16-17
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

class BST(Node):
    "Binary search tree class (with recursive insert, search)"

    def search(self, k, verbose=False):
        """
        Find a node in this tree with key `k` and return it;
        return None if no such node exists.
        """
        print("At",self,"searching for key",k)
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
                    print("Dead end; there is no node with key",k)
                return None
            else:
                if verbose:
                    print("Descending into left subtree")
                return self.left.search(k,verbose)
        elif self.key < k:
            # The node with key `k` must be in the right subtree
            if self.right == None:
                # Lack of right child means `k` is not present
                if verbose:
                    print("Dead end; there is no node with key",k)
                return None
            else:
                if verbose:
                    print("Descending into right subtree")
                return self.right.search(k,verbose)


    def insert(self, k):
        """
        Find a suitable place to add a new node to this BST
        with key `k`, and add it.
        """
        if self.key == None:
            # Empty tree, so just make this node have key `k`
            self.key = k
            return
        if k <= self.key:
            if self.left == None:
                # `k` belongs to the left, and the left is empty.
                # Create a new node and make it the left child
                node = BST(key=k)
                self.left = node
            else:
                # Have the left subtree handle it!
                self.left.insert(k)
        else:
            if self.right == None:
                # `k` belongs to the right, and the right is empty.
                # Create a new node and make it the right child
                node = BST(key=k)
                self.right = node
            else:
                # Have the right subtree handle it!
                self.right.insert(k)
