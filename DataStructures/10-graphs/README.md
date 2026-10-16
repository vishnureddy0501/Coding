# Graphs — Interview Roadmap

Learn in this order:

| Step | Topic | Files |
|---|---|---|
| 1 | Basics | [Representation](01-basics/01-representation.md), [BFS and DFS](01-basics/02-bfs-and-dfs.md), [Grid graphs](01-basics/03-grid-graphs.md) |
| 2 | Cycles | [Cycle detection](02-cycles-and-bipartite/01-cycle-detection.md), [Bipartite graph](02-cycles-and-bipartite/02-bipartite.md) |
| 3 | Dependencies | [Topological sort](03-topological-sort/01-topological-sort.md) |
| 4 | Shortest path | [Choose algorithm](04-shortest-path/01-choose-algorithm.md), [BFS and Dijkstra](04-shortest-path/02-bfs-and-dijkstra.md), [Other algorithms](04-shortest-path/03-other-shortest-paths.md) |
| 5 | Grouping and minimum cost | [Disjoint Set](05-dsu-and-mst/01-disjoint-set.md), [MST](05-dsu-and-mst/02-minimum-spanning-tree.md) |
| 6 | Practice | [Important problems](06-important-problems.md) |
| 7 | Revision | [Cheat sheet](07-cheat-sheet.md) |

## Patterns you must know

1. Build an adjacency list.
2. BFS and DFS.
3. Connected components and grid traversal.
4. Cycle detection in undirected and directed graphs.
5. Bipartite graph using two colors.
6. Topological sort using Kahn's algorithm.
7. BFS for unweighted shortest paths.
8. Dijkstra for non-negative weights.
9. Disjoint Set Union (DSU).
10. Minimum Spanning Tree using Prim or Kruskal.

Bellman-Ford, Floyd-Warshall, SCC, and bridges are lower priority. Understand when they are used; learn their code after the above topics.

## Quick decision guide

| Problem asks for | Use |
|---|---|
| Visit or count groups | BFS or DFS |
| Minimum moves, every move has equal cost | BFS |
| Spread from many starting points | Multi-source BFS |
| Dependencies or course ordering | Topological sort |
| Weighted shortest path, no negative weight | Dijkstra |
| Negative edge weights | Bellman-Ford |
| Connect all nodes with minimum total cost | MST |
| Repeatedly merge groups | DSU |

