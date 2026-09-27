# Graphs — Study Roadmap

Go folder by folder, file by file, in number order. Each step uses ideas from the steps before it.

## 01-basics
| # | File | What you learn |
|---|------|----------------|
| 1 | [GraphRepresentation](01-basics/01-GraphRepresentation.md) | Edge list vs adjacency list vs matrix, building the graph |
| 2 | [BFS](01-basics/02-BFS.md) | Queue traversal, level-wise BFS, multi-source BFS, grid BFS |
| 3 | [DFS](01-basics/03-DFS.md) | Recursive traversal, connected components, BFS vs DFS |
| 4 | [ImportantNotes](01-basics/04-ImportantNotes.md) | Quick tips |

## 02-cycles-and-bipartite (undirected graphs)
| # | File | What you learn |
|---|------|----------------|
| 1 | [DetectCycleUndirectedGraph](02-cycles-and-bipartite/01-DetectCycleUndirectedGraph.md) | BFS/DFS with parent tracking |
| 2 | [BipartiteGraph](02-cycles-and-bipartite/02-BipartiteGraph.md) | 2-coloring, odd cycle ⇒ not bipartite |

## 03-topological-sort (directed graphs)
| # | File | What you learn |
|---|------|----------------|
| 1 | [TopologicalSort](03-topological-sort/01-TopologicalSort.md) | DFS topo sort, Kahn's (BFS) algorithm, applications |
| 2 | [DetectCycleDirectedGraph](03-topological-sort/02-DetectCycleDirectedGraph.md) | DFS + recursion stack, Kahn's count check |

## 04-shortest-path
| # | File | What you learn |
|---|------|----------------|
| 1 | [ShortestPathUnitDistance](04-shortest-path/01-ShortestPathUnitDistance.md) | BFS for unit weights |
| 2 | [ShortestPathInDAG](04-shortest-path/02-ShortestPathInDAG.md) | Topo sort + relaxation |
| 3 | [Dijkstra](04-shortest-path/03-Dijkstra.md) | Priority queue, non-negative weights |
| 4 | [DijkstraDoubts](04-shortest-path/04-DijkstraDoubts.md) | Why store distance in the queue |
| 5 | [ShortestPathInBinaryMaze](04-shortest-path/05-ShortestPathInBinaryMaze.md) | Grid shortest path |
| 6 | [WordLadder2](04-shortest-path/06-WordLadder2.md) | BFS storing whole paths |
| 7 | [BellmanFord](04-shortest-path/07-BellmanFord.md) | Negative edges, negative-cycle detection |
| 8 | [FloydWarshall](04-shortest-path/08-FloydWarshall.md) | All-pairs shortest path + **which algorithm to pick** |

## 05-disjoint-set-and-mst
| # | File | What you learn |
|---|------|----------------|
| 1 | [Prims](05-disjoint-set-and-mst/01-Prims.md) | MST definition, Prim's with a min-heap |
| 2 | [DisjointSet](05-disjoint-set-and-mst/02-DisjointSet.md) | Union by rank/size, path compression |
| 3 | [Kruskals](05-disjoint-set-and-mst/03-Kruskals.md) | MST using sorted edges + DSU |
| 4 | [NumberOfProvinces](05-disjoint-set-and-mst/04-NumberOfProvinces.md) | Counting components with DSU |
| 5 | [SimilarStringGroups](05-disjoint-set-and-mst/05-SimilarStringGroups.md) | DSU on strings |
| 6 | [PracticeProblems](05-disjoint-set-and-mst/06-PracticeProblems.md) | More DSU problems |

## Advanced (later)
Kosaraju SCC and Bridges/Tarjan moved to [advanced-later/04-graphs](../advanced-later/04-graphs/).

## Cheat sheet
| Problem says… | Think… |
|---|---|
| minimum steps / moves, all edges cost 1 | BFS |
| spread from many starting points at once | Multi-source BFS |
| count islands / groups | DFS/BFS from each unvisited node, or DSU |
| ordering with dependencies (courses, tasks) | Topological sort |
| cycle in directed graph | DFS + recursion stack, or Kahn's |
| cycle in undirected graph | BFS/DFS with parent, or DSU |
| weighted shortest path, weights ≥ 0 | Dijkstra |
| negative weights | Bellman-Ford |
| distance between every pair | Floyd-Warshall |
| connect everything with minimum cost | MST (Prim's / Kruskal's) |
| edges keep getting added, "are u and v connected?" | Disjoint Set |
| critical edge / connection | Bridges (Tarjan) — see advanced-later |
