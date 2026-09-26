Graph Representation
--------------------
Graph = nodes (vertices) + edges.
    Directed   : u -> v   (one way)
    Undirected : u - v    (both ways, add edge in both directions)
    Weighted   : every edge has a cost

Input usually comes in one of these 3 forms. ALWAYS check which one the problem gives.
(Most "wrong answer" bugs in basic graph problems come from reading the input wrong.)

1. Edge list: vector<vector<int>> edges = {{0,1}, {1,2}}   -> each entry is ONE edge
    Build an adjacency list from it:

        vector<vector<int>> graph(n);
        for (auto &e : edges) {
            graph[e[0]].push_back(e[1]);
            graph[e[1]].push_back(e[0]);   // skip this line for directed graphs
        }

    Weighted edge list {u, v, w}:

        vector<vector<pair<int,int>>> graph(n);   // graph[u] = {v, w}
        for (auto &e : edges) {
            graph[e[0]].push_back({e[1], e[2]});
            graph[e[1]].push_back({e[0], e[2]});   // skip for directed
        }

2. Adjacency list: vector<vector<int>> adj  -> adj[i] = ALL neighbours of node i
    Already ready to use. Do NOT rebuild it (reading adj[i][0], adj[i][1] as an edge is wrong).

3. Adjacency matrix: adj[i][j] == 1 means edge i - j   (e.g. Number of Provinces)
    Loop over j for neighbours of i: O(V) per node.

Watch out for 1-based node numbers (1..n). Either subtract 1 while building or size arrays n + 1.

Space:
    Adjacency list   : O(V + E)   -> use this almost always
    Adjacency matrix : O(V * V)

Terms you should know:
    degree         : number of edges on a node (undirected). Sum of degrees = 2 * E
    indegree       : edges coming INTO a node (directed)
    outdegree      : edges going OUT of a node (directed)
    connected component : group of nodes reachable from each other
    DAG            : Directed Acyclic Graph (directed, no cycles)
    tree           : connected undirected graph with n nodes and n - 1 edges, no cycles
