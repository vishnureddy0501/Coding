# Vertical-Order Traversal

For every node, track:

- `x`: horizontal column
- `y`: depth or row

```text
root        → (0, 0)
left child  → (x - 1, y + 1)
right child → (x + 1, y + 1)
```

For LeetCode 987, values are sorted by:

1. Column
2. Row
3. Node value when positions are identical

Use:

```cpp
map<int, map<int, multiset<int>>> nodes;
```

## C++ Solution

```cpp
vector<vector<int>> verticalTraversal(TreeNode* root) {
    vector<vector<int>> result;
    if (root == nullptr) return result;

    queue<pair<TreeNode*, pair<int, int>>> pending;
    map<int, map<int, multiset<int>>> nodes;
    pending.push({root, {0, 0}});

    while (!pending.empty()) {
        auto [node, position] = pending.front();
        pending.pop();

        auto [x, y] = position;
        nodes[x][y].insert(node->val);

        if (node->left != nullptr) {
            pending.push({node->left, {x - 1, y + 1}});
        }

        if (node->right != nullptr) {
            pending.push({node->right, {x + 1, y + 1}});
        }
    }

    for (const auto& [x, rows] : nodes) {
        vector<int> column;

        for (const auto& [y, values] : rows) {
            column.insert(column.end(), values.begin(), values.end());
        }

        result.push_back(column);
    }

    return result;
}
```

## Complexity

Ordered insertion makes the complexity approximately `O(n log n)`. The data structures require `O(n)` space.

