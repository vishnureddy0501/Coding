# 1. Graph Basics and Representation

A graph contains:

- **Vertex/node:** an item.
- **Edge:** a connection between two items.

```text
Undirected: 0 -- 1        connection works both ways
Directed:   0 -> 1        connection works one way
Weighted:   0 --5-- 1     connection has cost 5
```

## Adjacency list

`graph[node]` stores its neighbors. Use this for most problems.

### Undirected graph

```cpp
vector<vector<int>> graph(n);

for (auto& edge : edges) {
    int u = edge[0];
    int v = edge[1];

    graph[u].push_back(v);
    graph[v].push_back(u);
}
```

Add both directions because `u -- v` works both ways.

### Directed graph

```cpp
vector<vector<int>> graph(n);

for (auto& edge : edges) {
    int from = edge[0];
    int to = edge[1];
    graph[from].push_back(to);
}
```

### Weighted graph

```cpp
vector<vector<pair<int, int>>> graph(n);

for (auto& edge : edges) {
    int u = edge[0];
    int v = edge[1];
    int weight = edge[2];

    graph[u].push_back({v, weight});
    graph[v].push_back({u, weight});
}
```

Each pair means `{neighbor, weight}`.

## Adjacency matrix

```cpp
vector<vector<int>> matrix(n, vector<int>(n, 0));
matrix[u][v] = 1;
```

Use it when the input already gives a matrix, such as Number of Provinces.

| Storage | Space |
|---|---|
| Adjacency list | `O(V + E)` |
| Adjacency matrix | `O(V²)` |

## Important terms

- **Degree:** number of edges connected to a node.
- **Indegree:** directed edges entering a node.
- **Outdegree:** directed edges leaving a node.
- **Path:** sequence of connected nodes.
- **Cycle:** a path that returns to its starting node.
- **Component:** a separate connected group.
- **DAG:** directed graph with no cycle.
- **Tree:** connected undirected graph with `V - 1` edges and no cycle.

## Input mistakes

- Check whether nodes are `0...n-1` or `1...n`.
- Do not add the reverse edge in a directed graph.
- An edge list and an adjacency list are different inputs.
- Use `long long` when total edge weights may exceed `int`.

