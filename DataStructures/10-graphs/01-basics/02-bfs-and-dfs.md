# 2. BFS and DFS

Both visit all reachable nodes in `O(V + E)` time.

## BFS

BFS visits level by level using a queue.

```text
0 -> {1, 2}
first visit 0, then 1 and 2
```

```cpp
void bfs(int start, vector<vector<int>>& graph, vector<int>& visited) {
    queue<int> q;
    q.push(start);
    visited[start] = 1;

    while (!q.empty()) {
        int node = q.front();
        q.pop();

        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = 1;
                q.push(neighbor);
            }
        }
    }
}
```

Mark a node visited when adding it to the queue. Otherwise, it may be added many times.

Use BFS for:

- Shortest path when every edge has equal cost.
- Minimum moves or steps.
- Level-by-level processing.
- Spreading from one or many sources.

## DFS

DFS goes deep and then comes back.

```cpp
void dfs(int node, vector<vector<int>>& graph, vector<int>& visited) {
    visited[node] = 1;

    for (int neighbor : graph[node]) {
        if (!visited[neighbor]) {
            dfs(neighbor, graph, visited);
        }
    }
}
```

Use DFS for:

- Components, islands, and paths.
- Cycle detection.
- Backtracking through all possible paths.
- Algorithms that need finishing order.

## Disconnected graph

Starting from node `0` may not visit every node. Use an outer loop:

```cpp
vector<int> visited(n, 0);

for (int node = 0; node < n; node++) {
    if (!visited[node]) {
        dfs(node, graph, visited);
    }
}
```

Each new traversal represents a new component.

## Important exception

Recursive DFS can overflow the call stack for a very deep graph. Use iterative DFS with `stack<int>` when constraints are very large.

