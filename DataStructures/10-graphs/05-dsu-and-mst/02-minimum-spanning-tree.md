# 11. Minimum Spanning Tree

An MST connects every node with:

- No cycle.
- Exactly `V - 1` edges.
- Minimum possible total cost.

It is defined for a connected, weighted, undirected graph.

## Prim's algorithm

Start from any node. Repeatedly take the cheapest edge that connects the built tree to an unvisited node.

```cpp
long long primMST(
    int n,
    vector<vector<pair<int, int>>>& graph
) {
    priority_queue<
        pair<int, int>,
        vector<pair<int, int>>,
        greater<pair<int, int>>
    > minHeap;

    vector<int> visited(n, 0);
    minHeap.push({0, 0}); // {edge weight, node}

    long long totalCost = 0;
    int nodesUsed = 0;

    while (!minHeap.empty()) {
        auto [weight, node] = minHeap.top();
        minHeap.pop();

        if (visited[node]) continue;

        visited[node] = 1;
        totalCost += weight;
        nodesUsed++;

        for (auto [neighbor, edgeWeight] : graph[node]) {
            if (!visited[neighbor]) {
                minHeap.push({edgeWeight, neighbor});
            }
        }
    }

    return nodesUsed == n ? totalCost : -1;
}
```

## Kruskal's algorithm

Sort all edges by weight. Add an edge only when it joins two different DSU groups.

```cpp
long long kruskalMST(int n, vector<vector<int>>& edges) {
    sort(edges.begin(), edges.end(), [](auto& a, auto& b) {
        return a[2] < b[2];
    });

    DisjointSet dsu(n);
    long long totalCost = 0;
    int edgesUsed = 0;

    for (auto& edge : edges) {
        int u = edge[0];
        int v = edge[1];
        int weight = edge[2];

        if (dsu.findParent(u) != dsu.findParent(v)) {
            dsu.unionSet(u, v);
            totalCost += weight;
            edgesUsed++;
        }
    }

    return edgesUsed == n - 1 ? totalCost : -1;
}
```

## Which one?

- Prim: natural when an adjacency list is given.
- Kruskal: natural when an edge list is given.

If the graph is disconnected, they create a minimum spanning forest, not one MST. The code above returns `-1` in that case.
