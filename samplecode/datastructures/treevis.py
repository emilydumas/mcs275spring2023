"""Functions for visualizing a tree structure"""
# MCS 275 Spring 2023 - Emily Dumas

def treeprint(root,*args,**kwargs):
    """
    Print a basic text-graphic representation of
    tree with root `root`.
    Optional formatting arguments:
        dots:  Set to False to hide missing nodes
               (otherwise they are shown as dots)
        trim:  Set to True to trim empty space and dots
               from left and right of the tree diagram
               to make it narrower.
    """
    print(treestr(root,*args,**kwargs))

def treestr(root,dots=True,trim=False):
    """
    Convert tree with root `root` to a text-graphic string.
    Optional formatting arguments:
        dots:  Set to False to hide missing nodes
               (otherwise they are shown as dots)
        trim:  Set to True to trim empty space and dots
               from left and right of the tree diagram
               to make it narrower.
    """
    s = ""
    L = level_lists(root)
    L = [ [node_str(x,dots=dots) for x in row] for row in L ]
    depth = len(L)
    maxlen = max( max(len(entry) for entry in row) for row in L )
    final_row_len = (maxlen)*(2**(depth-1))-1
    depth = len(L)
    lines = []
    for k,row in enumerate(L):
        width = (final_row_len - (2**k-1)) // 2**k
        s=" ".join(x.center(width) for x in row)
        lines.append(s.rstrip())
    if trim:
        leading_spaces = min(len(line) - len(line.lstrip(". ")) for line in lines)
        longest_content = max(len(line.rstrip(". ")) for line in lines)
        ntrim = max(0,leading_spaces-5)        
        lines = [ line[ntrim:longest_content+5] for line in lines ]
    spacers = reversed([ "\n"*(2+i//4) for i in range(len(lines)) ])
    return "".join( x+y for x,y in zip(lines,spacers) ).rstrip()+"\n"

def level_lists(node,L=None,n=0,idx=0):
    """Convert a tree into a list of lists, where
    the k^th list has 2**k elements that are either
    None or nodes of the original tree.  Each list
    represents one of the levels of the tree."""
    if node == None:
        return
    if L==None:
        L=[]
    if len(L)<=n:
        L.append([ None for _ in range(2**n) ])
    L[n][idx] = node
    level_lists(node.left,L,n+1,2*idx)
    level_lists(node.right,L,n+1,2*idx+1)
    return L

def node_str(x,dots=True):
    """Convert a node to a string, or convert None to
    the empty string or dot (depending on the value
    of the flag `dots`)"""
    if x == None:
        if dots:
            return "."
        else:
            return " "
    else:
        return str(x)