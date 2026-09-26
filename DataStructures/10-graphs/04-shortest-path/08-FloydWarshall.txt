Floyd-Warshall - shortest path between EVERY pair of nodes (multi-source)
--------------------------------------------------------------------------
Time: O(V^3)   Space: O(V^2)   -> fine for V <= ~400
Works with negative edges. Detects negative cycles.

Idea:
    dist[i][j] = shortest i -> j.
    For every node `via`, try going i -> via -> j and keep the smaller one.
    The `via` loop MUST be the outermost loop.

void floydWarshall(vector<vector<int>>& dist) {   // dist[i][j] = -1 means no edge
    int n = dist.size();
    const int INF = 1e9;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            if (dist[i][j] == -1) dist[i][j] = INF;
            if (i == j) dist[i][j] = 0;
        }

    for (int via = 0; via < n; via++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (dist[i][via] != INF && dist[via][j] != INF)
                    dist[i][j] = min(dist[i][j], dist[i][via] + dist[via][j]);

    // negative cycle: some dist[i][i] < 0

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (dist[i][j] == INF) dist[i][j] = -1;
}

Alternative: run Dijkstra from every node -> O(V * E log V). Faster for sparse graphs, but no negative edges.

Practice: "Find the City With the Smallest Number of Neighbors at a Threshold Distance" (LeetCode 1334)


Which shortest path algorithm?
-------------------------------
    Unit weights (all edges cost 1)     -> BFS                 O(V + E)
    DAG (weights may be negative)       -> Topo sort + relax   O(V + E)
    Non-negative weights                -> Dijkstra            O(E log V)
    Negative weights / detect neg cycle -> Bellman-Ford        O(V * E)
    All pairs                           -> Floyd-Warshall      O(V^3)
