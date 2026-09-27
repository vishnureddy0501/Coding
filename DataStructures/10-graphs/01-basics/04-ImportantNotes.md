# Important Graph Notes

## Visited Array

A boolean array is enough when a node has only two states: visited or not visited.

Use an integer array when more states are needed, such as:

```text
0 = unvisited
1 = currently on the DFS path
2 = completely processed
```

## Shortest Paths

### In a Tree

A tree has exactly one path between any two nodes. BFS or DFS can therefore find that path.

### In an Unweighted Graph

Use BFS for the shortest path. BFS explores nodes in increasing distance from the source.

Normal BFS and DFS traversal both take `O(V + E)`. DFS becomes exponential only when it deliberately explores every possible path by undoing visited state during backtracking.

## Choosing BFS or DFS

| Requirement | Preferred approach |
| --- | --- |
| Minimum steps in an unweighted graph | BFS |
| Level-by-level processing | BFS |
| Spread from multiple starting points | Multi-source BFS |
| Connected components | BFS or DFS |
| Explore all possible paths | DFS with backtracking |
| Topological ordering with finish time | DFS |

## Grid Problems

For Rotten Oranges, 01 Matrix, and similar spreading problems, push every starting source into the queue before beginning BFS.

For Number of Enclaves, start traversal from boundary land cells. Any land reached from the boundary is not an enclave.

