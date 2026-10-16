# 7. Choosing a Shortest-Path Algorithm

Do not use Dijkstra for every problem. First check the edge weights.

| Graph type | Algorithm | Time |
|---|---|---|
| Every edge has equal cost | BFS | `O(V + E)` |
| Weights are only `0` or `1` | 0-1 BFS | `O(V + E)` |
| Non-negative weights | Dijkstra | `O((V + E) log V)` |
| Weighted DAG, even with negative edges | Topological order | `O(V + E)` |
| Negative edges | Bellman-Ford | `O(V × E)` |
| Distance between every pair | Floyd-Warshall | `O(V³)` |

## Important difference

Shortest path and Minimum Spanning Tree are not the same.

- **Shortest path:** minimum cost from a source to another node.
- **MST:** minimum total cost to connect every node.

## Relaxation

Relaxation means improving a known distance:

```cpp
if (distance[neighbor] > distance[node] + weight) {
    distance[neighbor] = distance[node] + weight;
}
```

## Unreachable nodes

Initialize distances with a large value such as `LLONG_MAX`. Never calculate `LLONG_MAX + weight`; first check that the current node is reachable.

