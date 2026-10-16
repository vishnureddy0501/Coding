# 10. Disjoint Set Union (DSU)

DSU keeps track of separate groups.

It quickly answers:

- Are `a` and `b` in the same group?
- Merge the groups containing `a` and `b`.

## Example

```text
Initially: {0} {1} {2} {3}
unite(0, 1): {0, 1} {2} {3}
unite(1, 2): {0, 1, 2} {3}
```

## Interview-ready code

```cpp
class DisjointSet {
public:
    vector<int> parent;

    DisjointSet(int n) {
        for (int i = 0; i < n; i++) {
            parent.push_back(i);
        }
    }

    int findParent(int node) {
        if (parent[node] == node) {
            return node;
        }

        return parent[node] = findParent(parent[node]);
    }

    void unionSet(int u, int v) {
        int parentU = findParent(u);
        int parentV = findParent(v);

        if (parentU == parentV) {
            return;
        }

        parent[parentV] = parentU;
    }
};
```

## Why it is fast

**Path compression:** `findParent` directly connects nodes to their main parent, making future searches faster.

This is the simplest DSU version. Union by size is an optional optimization for later.

## Common uses

- Count components.
- Detect an extra edge by checking whether both nodes already have the same parent.
- Accounts Merge.
- Network connection problems.
- Kruskal's MST.

## Limitations

DSU is good when connections are added. Normal DSU does not easily support deleting an edge or finding the exact path between nodes.
