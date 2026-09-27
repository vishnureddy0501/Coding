DFS (Depth First Search) - go as deep as possible, then backtrack (recursion / stack)
-----------------------------------------------------------------------------------
Time: O(V + E)   Space: O(V) recursion stack

Standard code:

    void dfs(vector<vector<int>>& g, int node, vector<int>& visited, vector<int>& res) {
        visited[node] = 1;
        res.push_back(node);
        for (int nb : g[node]) {
            if (!visited[nb]) dfs(g, nb, visited, res);   // pass nb, NOT the loop index
        }
    }


BFS vs DFS - when to use which:
-------------------------------
    Shortest path in unweighted graph  -> BFS
    Level / minimum steps              -> BFS
    Cycle detection, components        -> either
    Topological sort, SCC, bridges     -> DFS (needs finish order / recursion)
    Explore all paths / backtracking   -> DFS


Practice: Number of Provinces, Number of Islands, Surrounded Regions, Number of Distinct Islands
