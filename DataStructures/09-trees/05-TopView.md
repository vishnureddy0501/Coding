# Top and Bottom Views

Assign a horizontal distance to every node:

```text
root        → 0
left child  → parent distance - 1
right child → parent distance + 1
```

## Top View

Use BFS and keep the first node seen at each horizontal distance.

## Bottom View

Use the same traversal but overwrite the value at each horizontal distance. The last node seen becomes visible from the bottom.

## C++ Template

```cpp
vector<int> topView(TreeNode* root) {
    vector<int> result;
    if (root == nullptr) return result;

    queue<pair<TreeNode*, int>> nodes;
    map<int, int> firstAtDistance;
    nodes.push({root, 0});

    while (!nodes.empty()) {
        auto [node, distance] = nodes.front();
        nodes.pop();

        if (!firstAtDistance.count(distance)) {
            firstAtDistance[distance] = node->val;
        }

        if (node->left != nullptr) {
            nodes.push({node->left, distance - 1});
        }

        if (node->right != nullptr) {
            nodes.push({node->right, distance + 1});
        }
    }

    for (const auto& [distance, value] : firstAtDistance) {
        result.push_back(value);
    }

    return result;
}
```

For bottom view, replace the first-seen condition with:

```cpp
firstAtDistance[distance] = node->val;
```

## Complexity

- Time: `O(n log n)` with an ordered map
- Space: `O(n)`

