# 5. Bipartite Graph

A graph is bipartite when every node can be colored with one of two colors and connected nodes always have different colors.

```text
0 -- 1 -- 2 -- 3
R    B    R    B       valid
```

A graph with an odd-length cycle is not bipartite.

## BFS solution

```cpp
bool colorComponent(
    int start,
    vector<vector<int>>& graph,
    vector<int>& color
) {
    queue<int> q;
    q.push(start);
    color[start] = 0;

    while (!q.empty()) {
        int node = q.front();
        q.pop();

        for (int neighbor : graph[node]) {
            if (color[neighbor] == -1) {
                color[neighbor] = 1 - color[node];
                q.push(neighbor);
            } else if (color[neighbor] == color[node]) {
                return false;
            }
        }
    }

    return true;
}

bool isBipartite(vector<vector<int>>& graph) {
    int n = graph.size();
    vector<int> color(n, -1);

    for (int node = 0; node < n; node++) {
        if (color[node] == -1 && !colorComponent(node, graph, color)) {
            return false;
        }
    }

    return true;
}
```

Color values:

```text
-1 = not colored
 0 = first color
 1 = second color
```

Remember to check every component. A disconnected component may contain an odd cycle.

