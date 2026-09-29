Bellman-Ford - single source shortest path that WORKS with negative edges
--------------------------------------------------------------------------
Use it when: edges can be negative, or you must detect a negative cycle.
Time: O(V * E)  (slower than Dijkstra's O(E log V))

Idea:
    A shortest path has at most V - 1 edges.
    So relax every edge V - 1 times. After that, all distances are final.
    Relax once more: if any distance still decreases -> negative cycle.

Works on directed graphs. For an undirected graph, add both directions
(then any negative edge is itself a negative cycle).

vector<int> bellmanFord(int n, vector<vector<int>>& edges, int src) {
    vector<int> dist(n, 1e8);
    dist[src] = 0;
    for (int i = 0; i < n - 1; i++) {
        for (auto &e : edges) {
            int u = e[0], v = e[1], w = e[2];
            if (dist[u] != 1e8 && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }
    // n-th relaxation: negative cycle check
    for (auto &e : edges) {
        int u = e[0], v = e[1], w = e[2];
        if (dist[u] != 1e8 && dist[u] + w < dist[v]) {
            return {-1};
        }
    }
    return dist;
}

Why check dist[u] != 1e8? An unreachable node plus a negative edge would wrongly "improve" another node.

Related: "Cheapest Flights Within K Stops" = Bellman-Ford with at most K + 1 rounds
(copy dist into a temp array each round). Striver solves it with a BFS on {stops, node, cost}.
See 04-DijkstraDoubts.md.
