Yes. You can solve all three using BFS with Kahn’s algorithm:(No need to learn DFS)

- Course Schedule I: determine whether all courses can be completed.
- Course Schedule II: return a valid course order.
- Directed graph cycle detection: determine whether a cycle exists.


Topological Sort: (it works for not connected graph also)
-------------------- 
Linear Ordering of vertices, such that if there is a edge between u & v then u shoule appear before v in the Ordering.

it exists in only directed acyclic graph. (directed graph without cycles)

a DAG must have one or more nodes with indegree 0. and 
DAG must have one or more nodes with outdegree 0.
Longest path b/w 2 nodes in a DAG must be finite.


Using Bfs (Kahn's Algorithm):
-----------------------------
1. Compute indegree of every node.
2. Push all nodes with indegree 0 into a queue.
3. Pop a node, add it to the answer, decrease indegree of its neighbours.
   Any neighbour that reaches indegree 0 goes into the queue.
4. If the answer has fewer than n nodes -> graph has a cycle (no topo order).

#include <bits/stdc++.h> 
vector<int> topologicalSort(vector<vector<int>> &edges, int n, int e)  {
    vector<vector<int>> graph(n);
    vector<int> indegree(n, 0);
    for (auto it : edges) {
        graph[it[0]].push_back(it[1]);
        indegree[it[1]]++;
    }
    queue<int> q;
    for (int i = 0; i < n; i++) {
        if (indegree[i] == 0) {
            q.push(i);
        }
    }
    vector<int> res;
    while(q.size() > 0) {
        auto it = q.front();
        q.pop();
        res.push_back(it);
        for (auto neighbour: graph[it]) {
            indegree[neighbour]--;
            if (indegree[neighbour] == 0) {
                q.push(neighbour);
            }
        }
    }
    return res;
}


Where is topo sort used?
------------------------
    Course Schedule I / II      (can you finish all courses? in what order?)
    Detect cycle in a directed graph
    Shortest path in a DAG      (04-shortest-path/02-ShortestPathInDAG.md)
    Alien Dictionary            (build graph from adjacent words, then topo sort)
    Find Eventual Safe States   (reverse the graph + Kahn's)


No need:
--------
Using Dfs:
----------
#include <bits/stdc++.h> 
void dfs(vector<vector<int>>& graph, vector<int>& visited, vector<int>& st, int index) {
    visited[index] = 1;
    for (int i = 0; i<graph[index].size(); i++) {
        if (visited[graph[index][i]] == 0) {
            dfs(graph, visited, st, graph[index][i]);
        }
    }
    st.push_back(index);
}
vector<int> topologicalSort(vector<vector<int>> &edges, int n, int e)  {
    vector<vector<int>> graph(n);
    for (int i = 0; i<edges.size(); i++) {
        graph[edges[i][0]].push_back(edges[i][1]);
    }
    vector<int> st;
    vector<int> visited(n, 0);
    for (int i = 0; i<n; i++) {
        if (visited[i] == 0) {
            dfs(graph, visited, st, i);
        }
    }
    reverse(st.begin(), st.end());
    return st;
}
