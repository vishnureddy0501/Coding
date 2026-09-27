1. using bfs [learn bfs it is enough]
--------------
#include<bits/stdc++.h>
using namespace std;
string bfs(vector<vector<int>>& graph, int n, vector<int>& visited, int index) {
    queue<pair<int, int>> q; // node, parent
    q.push({ index, -1 });
    visited[index] = 1;
    while(q.size() > 0) {
        auto it = q.front();
        q.pop();
        for (auto neighbour : graph[it.first]) {
            if (visited[neighbour] == 0) {
                visited[neighbour] = 1;
                q.push({ neighbour, it.first });
            } else {
                if (neighbour != it.second) {
                    // neighbour, parent same. hene cycle
                    return "Yes";
                }
            }
        }
    }
    return "No";
}

string cycleDetection (vector<vector<int>>& edges, int n, int m)
{
    vector<vector<int>> graph(n);
    vector<int> visited(n, 0);
    for (auto it : edges) {
        graph[it[0]-1].push_back(it[1]-1);
        graph[it[1]-1].push_back(it[0]-1);
    }
    for (int i = 0; i < n; i++) {
        if (visited[i] == 0) {
            string res = bfs(graph, n, visited, i);
            if (res == "Yes") return res;
        }
    }
    return "No";
}



2. DFS: [Optional]
-------------------

    #include <bits/stdc++.h>
    using namespace std;

    bool dfs(vector<vector<int>>& graph, vector<bool>& visited, int node, int parent) {
        visited[node] = true;

        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                if (dfs(graph, visited, neighbor, node)) {
                    return true;
                }
            } else {
                if (neighbor != parent) {
                    // Visited neighbor that's not the parent → cycle
                    return true;
                }
            }
        }

        return false;
    }

    string cycleDetection(vector<vector<int>>& edges, int n, int m) {
        vector<vector<int>> graph(n);
        for (auto& edge : edges) {
            int u = edge[0] - 1;
            int v = edge[1] - 1;
            graph[u].push_back(v);
            graph[v].push_back(u);
        }

        vector<bool> visited(n, false);
        for (int i = 0; i < n; ++i) {
            if (!visited[i]) {
                if (dfs(graph, visited, i, -1)) {
                    return "Yes";
                }
            }
        }

        return "No";
    }
