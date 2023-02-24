# treeutil

Module for generating random binary trees and binary search trees.

## Functions meant to be imported from this module


### `random_bst(nodes=6,seed=None)`
Generate a binary search tree with `nodes` distinct integer keys.  If `seed` is given, use it as the  seed for the random number generator (to make it possible to reproduce the same tree again later, if desired).

Sample usage:
```python
import treevis
import treeutil
T = treeutil.random_bst(nodes=5,seed=21)
treevis.treeprint(T)
```

Expected output:
```
      [13]

  [6]     [17]

[2] [10]  .   .
```

### `random_bst_and_node(nodes=6,seed=None)`
Make a BST and return the tree and a randomly selected node in that tree.  If `seed` is given, use it as the  seed for the random number generator (to make it possible to reproduce the same tree again later, if desired).

Sample usage:
```python
import treevis
import treeutil
T,x = treeutil.random_bst_and_node(nodes=5,seed=20)
treevis.treeprint(T)
print("\nThe selected node was",x)
```

Expected output:
```
             [9]

      [2]             [11]

   .      [6]      .       .

 .   .  [5]  .   .   .   .   .

The selected node was [11]
```


### `random_bst_and_node_pair(nodes=6,seed=None,distinct=False)`
Make a BST and return the tree and two randomly selected nodes in that tree.  If `distinct` is True, then two distinct nodes will be returned, while if `distinct` is False (the default), there is a chance that the two returned nodes will be the same.  If `seed` is given, use it as the  seed for the random number generator (to make it possible to reproduce the same tree again later, if desired).

Sample usage:
```python
import treevis
import treeutil
T,x,y = treeutil.random_bst_and_node_pair(nodes=7,distinct=True)
treevis.treeprint(T)
print("\nSelected nodes:",x,"and",y)
```


### `random_int_tree(nodes=6,distinct=False,seed=None)`
Generate a random binary tree where the nodes have integer keys.  Typically, the returned tree will not be a BST.  Keys may appear more than once, unless `distinct` is True.  If an integer is given as `seed`, the Random number generator will be seeded with that value (allowing the same random tree to be produced again).

Sample usage:
```python
import treevis
import treeutil
T = treeutil.random_int_tree(nodes=5,distinct=True,seed=320)
treevis.treeprint(T)
```

Expected output:
```
              [9]

      [4]              .

  [12]    [13]     .       .

 .   .  [5]  .   .   .   .   .
```

### `random_word_tree(nodes=6,distinct=False,seed=None)`
Identical to `random_int_tree` except the keys are common 5-letter English words rather than integers.

Sample usage:
```python
import treevis
import treeutil
T = treeutil.random_word_tree(nodes=5,distinct=True,seed=275)
treevis.treeprint(T)
```

Expected output:
```
                        [paper]

          [chair]                        .

   [quine]       [waste]          .             .

[entry]   .      .      .      .      .      .      .
```



### `random_treeify(keys,R=None)`

Turn list `keys` into a binary tree in a random way.  If a Random object `R` is provided, use it for the random number generation.

Sample usage:
```python
import treevis
import treeutil
T = treeutil.random_treeify(["apple",21,False,"green",6,8,12.2])
treevis.treeprint(T)
```