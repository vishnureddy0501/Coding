# Graphs Cheat Sheet

## Complexity

| Operation | Time |
|---|---|
| BFS / DFS | `O(V + E)` |
| Topological sort | `O(V + E)` |
| Dijkstra with heap | `O((V + E) log V)` |
| Bellman-Ford | `O(V × E)` |
| Floyd-Warshall | `O(V³)` |
| Kruskal | `O(E log E)` |
| Prim with heap | `O(E log V)` |

## Problem clue → technique

```text
groups / islands                 -> BFS or DFS
minimum steps, equal cost        -> BFS
many starting points spread      -> multi-source BFS
dependency order                 -> topological sort
weighted shortest path           -> Dijkstra
negative edge                    -> Bellman-Ford
connect everything cheaply       -> MST
merge groups / extra connection  -> DSU
```

## Common mistakes

- Forgetting the outer loop for disconnected graphs.
- Adding only one direction for an undirected edge.
- Adding both directions for a directed edge.
- Marking BFS nodes visited only after removing them from the queue.
- Using undirected parent logic for a directed cycle.
- Using Dijkstra with a negative edge.
- Forgetting to skip stale Dijkstra heap entries.
- Calculating `INF + weight`.
- Using `int` when total distance needs `long long`.
- Assuming topological order is unique.
- Returning an MST cost without checking that all nodes were connected.
- Forgetting grid boundary checks.

## Final revision order

```text
Representation
 -> BFS / DFS
 -> Grids and components
 -> Cycles and bipartite
 -> Topological sort
 -> BFS shortest path
 -> Dijkstra
 -> DSU
 -> MST
```
