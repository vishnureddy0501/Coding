# Detect a Cycle in a Directed Graph

## Why Not Use `visited + parent`?
    In a directed graph, reaching an already visited node does NOT always mean a cycle.
    e.g. 0->1, 0->2, 1->2 : node 2 is reached twice but there is no cycle.
    A cycle exists only if the visited node is still on the current DFS path (inStack).

Course Schedule I is the best example

🔹 2. Kahn’s Algorithm (BFS / Topological Sort)
--------------------------------------------------
Topological sort using BFS known as Kahn’s Algorithm

Uses Indegree

solution:
    compute topological sort vector.
    if toposort.size() < numbe of nodes 
        then the graph contains cycle
        because you are not able to print all nodes.
    if toposort.size() == number of nodes.
        no cycle. because you are able to print all nodes.





No Need:
-------
1. DFS (Depth-First Search) with Recursion Stack

    Idea:
        Maintain
            visited[node]: whether node is visited at all.
            inStack[node]: whether node is currently in the DFS recursion stack.
        If during DFS we find a neighbor that is already in the recursion stack → cycle exists.

    class Solution {
    public:
        bool dfs(int node, vector<vector<int>>& adj, vector<int>& visited, vector<int>& inStack) {
            visited[node] = 1;
            inStack[node] = 1;

            for (int nei : adj[node]) {
                if (!visited[nei]) {
                    if (dfs(nei, adj, visited, inStack)) return true;
                } else {
                    if (inStack[nei]) {
                        return true; // found back edge -> cycle
                    }
                }
            }

            inStack[node] = 0; // remove from recursion stack
            return false;
        }

        bool hasCycle(int n, vector<vector<int>>& adj) {
            vector<int> visited(n, 0), inStack(n, 0);

            for (int i = 0; i < n; i++) {
                if (!visited[i]) {
                    if (dfs(i, adj, visited, inStack)) return true;
                }
            }
            return false;
        }
    };

