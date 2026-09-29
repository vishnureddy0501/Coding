# Construct a Binary Tree from Traversals

## Preorder and Inorder

- Preorder identifies the root first.
- Inorder separates the left and right subtrees.
- A unique tree can be constructed when values are distinct.

## Postorder and Inorder

- Postorder identifies the root last.
- Inorder separates the left and right subtrees.
- A unique tree can be constructed when values are distinct.

## Preorder and Postorder

These traversals do not generally identify a unique binary tree. Multiple trees can produce the same preorder and postorder sequences.

A unique result requires additional rules, such as the tree being full.

## Efficient Approach

Store every inorder value and its index in a hash map. This avoids scanning the inorder array during every recursive call.

With distinct values:

- Time: `O(n)`
- Extra space: `O(n)`
- Recursion space: `O(h)`

## Interview Pattern

For every recursive call:

1. Identify the root from preorder or postorder.
2. Find the root position in inorder.
3. Calculate the left subtree size.
4. Recursively construct the left and right subtrees.

