# 8. BFS and Dijkstra

## Unweighted shortest path

Every edge costs `1`, so BFS reaches nodes in shortest-distance order.

```cpp
vector<int> shortestPathUnweighted(
    int n,
    vector<vector<int>>& graph,
    int source
) {
    vector<int> distance(n, -1);
    queue<int> q;

    distance[source] = 0;
    q.push(source);

    while (!q.empty()) {
        int node = q.front();
        q.pop();

        for (int neighbor : graph[node]) {
            if (distance[neighbor] == -1) {
                distance[neighbor] = distance[node] + 1;
                q.push(neighbor);
            }
        }
    }

    return distance;
}
```

## Dijkstra

Use it when edge weights are non-negative.

```cpp
vector<long long> dijkstra(
    int n,
    vector<vector<pair<int, int>>>& graph,
    int source
) {
    const long long INF = LLONG_MAX;
    vector<long long> distance(n, INF);

    priority_queue<
        pair<long long, int>,
        vector<pair<long long, int>>,
        greater<pair<long long, int>>
    > minHeap;

    distance[source] = 0;
    minHeap.push({0, source});

    while (!minHeap.empty()) {
        auto [currentDistance, node] = minHeap.top();
        minHeap.pop();

        if (currentDistance != distance[node]) continue;

        for (auto [neighbor, weight] : graph[node]) {
            long long newDistance = currentDistance + weight;

            if (newDistance < distance[neighbor]) {
                distance[neighbor] = newDistance;
                minHeap.push({newDistance, neighbor});
            }
        }
    }

    return distance;
}
```

The heap stores `{distance, node}` so the smallest known distance is processed first.

## Important exceptions

- Dijkstra works with zero-weight edges.
- Dijkstra does not work with negative-weight edges.
- The same node may enter the heap many times. Skip old entries with the stale-entry check.
- To return the actual path, store `parent[neighbor] = node` whenever its distance improves.

