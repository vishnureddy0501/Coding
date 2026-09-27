# Tree Introduction

## Types of Binary Trees

### Full Binary Tree

Every node has either zero or two children.

### Complete Binary Tree

Every level is completely filled except possibly the last level. Nodes on the last level are filled from left to right.

### Perfect Binary Tree

Every internal node has two children, and all leaves are at the same level.

For height `h`, where the root is level 1:

```text
number of nodes = 2^h - 1
```

### Balanced Binary Tree

For every node, the heights of the left and right subtrees differ by at most one. Its height remains approximately `O(log n)`.

### Degenerate or Skewed Tree

Every node has only one child. It behaves like a linked list and can have height `O(n)`.

## Traversals

```text
Preorder:    root, left, right
Inorder:     left, root, right
Postorder:   left, right, root
Level order: breadth-first search with a queue
```

Inorder traversal produces sorted values only for a Binary Search Tree.

## Important Patterns

### Diameter of a Binary Tree

Calculate height and diameter in the same postorder traversal. Recalculating height at every node can produce an `O(n²)` solution.

### Boundary Traversal

Process:

1. Left boundary without leaves
2. All leaf nodes
3. Right boundary without leaves, in reverse order

Avoid adding the root or leaf nodes more than once.

### Vertical-Order Traversal

Track a horizontal coordinate, vertical level, and node value. A useful ordered structure is:

```cpp
map<int, map<int, multiset<int>>> nodes;
```

It sorts by column, then row, then node value.

