# 4. Cycle Detection

Undirected and directed graphs need different methods.

## Undirected graph: BFS with parent

When moving from `parent` to `node`, seeing the parent again is normal. Seeing any other visited neighbor means a cycle.

```cpp
bool hasCycleFrom(
    int start,
    vector<vector<int>>& graph,
    vector<int>& visited
) {
    queue<pair<int, int>> q;
    q.push({start, -1});
    visited[start] = 1;

    while (!q.empty()) {
        auto [node, parent] = q.front();
        q.pop();

        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = 1;
                q.push({neighbor, node});
            } else if (neighbor != parent) {
                return true;
            }
        }
    }

    return false;
}

bool hasUndirectedCycle(int n, vector<vector<int>>& graph) {
    vector<int> visited(n, 0);

    for (int node = 0; node < n; node++) {
        if (!visited[node] && hasCycleFrom(node, graph, visited)) {
            return true;
        }
    }

    return false;
}
```

## Directed graph: Kahn's algorithm

Try to create a topological order. If fewer than `n` nodes are processed, a cycle exists.

```cpp
bool hasDirectedCycle(int n, vector<vector<int>>& graph) {
    vector<int> indegree(n, 0);

    for (int node = 0; node < n; node++) {
        for (int neighbor : graph[node]) {
            indegree[neighbor]++;
        }
    }

    queue<int> q;
    for (int node = 0; node < n; node++) {
        if (indegree[node] == 0) q.push(node);
    }

    int processed = 0;

    while (!q.empty()) {
        int node = q.front();
        q.pop();
        processed++;

        for (int neighbor : graph[node]) {
            indegree[neighbor]--;
            if (indegree[neighbor] == 0) q.push(neighbor);
        }
    }

    return processed != n;
}
```

## Do not mix the rules

- Undirected graph: track the parent.
- Directed graph: use Kahn's algorithm or DFS path states.
- A visited node in a directed graph does not automatically mean a cycle.

The parent method assumes a normal simple graph. For duplicate parallel edges, clarify whether two such edges count as a cycle.

