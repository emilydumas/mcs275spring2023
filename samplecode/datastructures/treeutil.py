"""Generate random trees for testing"""
# MCS 275 Spring 2023 - David Dumas
from trees import Node, BST
import random


def random_distinct_integers(n,R=None):
    """
    Return a list of random distinct integers with gaps between
    closest pairs approximately 2 + (n/20).
    """
    if R == None:
        R = random
    L = []
    x = 1+R.randrange(n)
    for _ in range(n):
        L.append(x)
        x += 1 + R.randrange(4 + n//10)
    R.shuffle(L)
    return L


def random_treeify(keys,R=None):
    """
    Turn list `keys` into a binary tree in a random way, using Random
    object `R` to provide the entropy (if given).
    """
    if R==None:
        R = random
    if not keys:
        return None
    x = Node(keys.pop())
    if keys:
        p = R.randint(0,len(keys))
        lkeys = keys[:p]
        rkeys = keys[p:]
        x.left = random_treeify(lkeys,R)
        x.right = random_treeify(rkeys,R)
    return x


def random_int_tree(nodes=6,distinct=False,seed=None):
    """
    Generate a random binary tree where the nodes have
    integer keys.  Not a BST in most cases!
    """
    if seed == None:
        R = random
    else:
        R = random.Random(seed)
    if distinct:
        keys = random_distinct_integers(nodes,R=R)
    else:
        keys = [ random.randint(1,2*nodes) for _ in range(nodes) ]

    return random_treeify(keys,R)


def random_word_tree(nodes=6,distinct=False,seed=None):
    """
    Generate a random binary tree where the nodes have
    5-letter words as keys.  Not a BST in most cases!
    """
    if seed == None:
        R = random
    else:
        R = random.Random(seed)
    if distinct:
        keys = R.sample(_wordlist,k=nodes)
    else:
        keys = R.choices(_wordlist,k=nodes)
    return random_treeify(keys,R)


def random_bst(nodes=6,seed=None):
    """
    Generate a BST by inserting `nodes` distinct values
    in random order.  If `seed` is given, use it as the 
    seed for the random number generator (to make it possible
    to reproduce the same tree again later, if desired).
    """
    if seed == None:
        R = random
    else:
        R = random.Random(seed)
    x = 1+R.randrange(nodes)
    T = BST()
    keys = []
    for _ in range(nodes):
        keys.append(x)
        x += 1 + R.randrange(4 + nodes//10)
    R.shuffle(keys)
    T.key = keys.pop()
    while keys:
        T.insert(keys.pop())
    return T


def random_bst_and_node(nodes=6,seed=None):
    """Return a random BST and a node in it."""
    T,x,y = random_bst_and_node_pair(nodes=nodes,seed=seed,distinct=False)
    return T,x


def random_bst_and_node_pair(nodes=6,seed=None,distinct=False):
    """Return a random BST and two nodes in that tree.  If 
    `distinct` is True, the two nodes returned will be distinct."""
    if distinct and nodes<2:
        raise ValueError("Impossible to select two distinct nodes in a tree with {} nodes".format(nodes))
    T = random_bst(nodes=nodes,seed=seed)
    # NOTE: It *is* possible to select nodes at random using a bounded amount of temporary storage,
    # but here we instead use a more easily understood method that enumerates all nodes in a list
    # (using storage proportional to total size of tree).
    if seed == None:
        R = random
    else:
        R = random.Random(seed)
    L = tree_node_list(T)
    if distinct:
        x,y=R.sample(L,k=2)  # Random.sample chooses items without replacement
    else:
        x,y=R.choices(L,k=2) # Random.choices chooses items with replacement
    return T,x,y


def tree_node_list(x):
    """
    Return a list of node `x` and all its descendants.
    """
    if x == None:
        return []
    L=[x]
    L.extend(tree_node_list(x.left))  # list.extend is like a faster += for lists
    L.extend(tree_node_list(x.right))
    return L


# 200 5-letter words
_wordlist = ['chain', 'train', 'north', 'sight', 'field', 'event', 'place', 'sugar', 'total', 'music', 'shirt', 'squad', 'focus', 'input', 'staff', 'sorts', 'horse', 'visit', 'lunch', 'state', 'order', 'score', 'thing', 'unity', 'trend', 'theme', 'terry', 'pitch', 'break', 'floor', 'piece', 'quine', 'truth', 'chest', 'steam', 'peace', 'power', 'smoke', 'frame', 'depth', 'grant', 'sleep', 'dance', 'start', 'mouth', 'smile', 'world', 'cross', 'other', 'cause', 'shift', 'drive', 'fight', 'water', 'steel', 'green', 'court', 'error', 'white', 'trade', 'plate', 'coast', 'night', 'draft', 'crime', 'press', 'judge', 'scope', 'award', 'uncle', 'pride', 'phone', 'chief', 'peter', 'march', 'board', 'route', 'sport', 'sound', 'offer', 'tower', 'ratio', 'union', 'doubt', 'final', 'title', 'index', 'brown', 'layer', 'motor', 'while', 'touch', 'fault', 'radio', 'stuff', 'paper', 'issue', 'basis', 'party', 'anger', 'proof', 'track', 'youth', 'plant', 'novel', 'pilot', 'river', 'money', 'stock', 'owner', 'video', 'crown', 'heart', 'skill', 'block', 'range', 'dream', 'plane', 'trust', 'fruit', 'trial', 'group', 'store', 'model', 'right', 'round', 'watch', 'point', 'noise', 'image', 'stone', 'table', 'major', 'metal', 'drink', 'drama', 'child', 'class', 'clock', 'south', 'shape', 'knife', 'scene', 'study', 'birth', 'buyer', 'waste', 'cycle', 'space', 'level', 'sheep', 'grass', 'shock', 'brain', 'slake', 'taste', 'smith', 'reply', 'light', 'queen', 'style', 'cream', 'apple', 'crowd', 'force', 'limit', 'dress', 'nurse', 'earth', 'voice', 'sense', 'cover', 'front', 'phase', 'hotel', 'prize', 'value', 'spite', 'panel', 'pound', 'sheet', 'house', 'match', 'agent', 'claim', 'glass', 'chair', 'enemy', 'bread', 'share', 'stage', 'guide', 'whole', 'coach', 'entry', 'month', 'beach', 'scale', 'price', 'speed']
