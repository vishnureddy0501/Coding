# 9. Other Shortest-Path Algorithms

These are lower priority but important to recognize.

## Shortest path in a DAG

1. Find topological order.
2. Set the source distance to `0`.
3. Process nodes in topological order.
4. Relax every outgoing edge once.

It supports negative edges because a DAG has no cycles.

## Bellman-Ford

Use it for a single source when negative edges are present.

```cpp
vector<long long> bellmanFord(
    int n,
    vector<vector<int>>& edges,
    int source
) {
    const long long INF = LLONG_MAX;
    vector<long long> distance(n, INF);
    distance[source] = 0;

    for (int round = 1; round <= n - 1; round++) {
        bool changed = false;

        for (auto& edge : edges) {
            int from = edge[0];
            int to = edge[1];
            int weight = edge[2];

            if (distance[from] != INF &&
                distance[from] + weight < distance[to]) {
                distance[to] = distance[from] + weight;
                changed = true;
            }
        }

        if (!changed) break;
    }

    return distance;
}
```

If a distance can still improve in the `n`th round, a reachable negative cycle exists.

## Floyd-Warshall

Use it when distances are needed between every pair of nodes and `n` is small.

```cpp
for (int via = 0; via < n; via++) {
    for (int from = 0; from < n; from++) {
        for (int to = 0; to < n; to++) {
            if (distance[from][via] != INF &&
                distance[via][to] != INF) {
                distance[from][to] = min(
                    distance[from][to],
                    distance[from][via] + distance[via][to]
                );
            }
        }
    }
}
```

After the algorithm, `distance[i][i] < 0` means a negative cycle affects node `i`.

## 0-1 BFS

When weights are only `0` and `1`, use a deque:

- Weight `0`: add the neighbor to the front.
- Weight `1`: add the neighbor to the back.

It is faster than Dijkstra for this special case.

