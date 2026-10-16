# 6. Topological Sort

Topological sort gives an order for tasks with dependencies.

```text
A -> B means A must come before B
```

It works only for a **Directed Acyclic Graph (DAG)**.

## Kahn's algorithm

`indegree[node]` means the number of unfinished requirements for that node.

```text
1. Count indegrees.
2. Add all nodes with indegree 0 to the queue.
3. Process one node and remove its outgoing edges.
4. A neighbor enters the queue when its indegree becomes 0.
```

```cpp
vector<int> topologicalSort(int n, vector<vector<int>>& graph) {
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

    vector<int> order;

    while (!q.empty()) {
        int node = q.front();
        q.pop();
        order.push_back(node);

        for (int neighbor : graph[node]) {
            indegree[neighbor]--;
            if (indegree[neighbor] == 0) q.push(neighbor);
        }
    }

    if (order.size() != n) return {}; // cycle
    return order;
}
```

## Important points

- A graph may have multiple valid topological orders.
- An empty result here means the graph contains a cycle.
- It also works when the DAG has disconnected parts.
- A DAG always has at least one node with indegree `0`.

## Common problems

- Course Schedule I: check whether all nodes are processed.
- Course Schedule II: return the order.
- Alien Dictionary: build character dependencies, then topological sort.
- Eventual Safe States: reverse edges and use Kahn's algorithm.

