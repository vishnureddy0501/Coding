# Shortest Path in a DAG

Find the shortest distance from one source to every node in a weighted Directed Acyclic Graph.

## Why Topological Order Works

When a node is processed in topological order, all paths entering it have already been considered. We can safely relax its outgoing edges once.

This works with negative edge weights because a DAG has no cycle. Dijkstra does not support negative weights.

## Steps

1. Build the weighted directed adjacency list.
2. Find a topological ordering.
3. Set the source distance to `0` and all others to infinity.
4. Process nodes in topological order and relax outgoing edges.
5. Convert unreachable distances to `-1` if required.

## C++ Solution

```cpp
void topoDfs(
    int node,
    const vector<vector<pair<int, int>>>& graph,
    vector<bool>& visited,
    vector<int>& order
) {
    visited[node] = true;

    for (auto [neighbor, weight] : graph[node]) {
        if (!visited[neighbor]) {
            topoDfs(neighbor, graph, visited, order);
        }
    }

    order.push_back(node);
}

vector<int> shortestPathInDAG(
    int nodeCount,
    const vector<vector<int>>& edges,
    int source
) {
    vector<vector<pair<int, int>>> graph(nodeCount);

    for (const auto& edge : edges) {
        int from = edge[0];
        int to = edge[1];
        int weight = edge[2];
        graph[from].push_back({to, weight});
    }

    vector<bool> visited(nodeCount, false);
    vector<int> order;

    for (int node = 0; node < nodeCount; node++) {
        if (!visited[node]) {
            topoDfs(node, graph, visited, order);
        }
    }

    reverse(order.begin(), order.end());

    const int INF = 1e9;
    vector<int> distance(nodeCount, INF);
    distance[source] = 0;

    for (int node : order) {
        if (distance[node] == INF) continue;

        for (auto [neighbor, weight] : graph[node]) {
            distance[neighbor] = min(
                distance[neighbor],
                distance[node] + weight
            );
        }
    }

    for (int& value : distance) {
        if (value == INF) value = -1;
    }

    return distance;
}
```

## Important Mistake

Never calculate `INF + weight`. Skip unreachable nodes before relaxing their edges to avoid overflow and invalid distances.

## Complexity

- Time: `O(V + E)`
- Space: `O(V + E)`

