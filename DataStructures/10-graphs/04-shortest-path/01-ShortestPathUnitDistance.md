# Shortest Path in an Unweighted Graph

[Practice problem](https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph-having-unit-distance/1)

Every edge has cost `1`, so BFS finds the shortest distance from the source to every reachable node.

class Solution {
  public:
    int shortestPath(int n, vector<vector<int>> &edges, int src, int dest) {
        vector<vector<int>> graph(n);
		vector<int> distance(n, INT_MAX);
		for(auto edge : edges) {
		     graph[edge[0]].push_back(edge[1]);
		     graph[edge[1]].push_back(edge[0]);
	    }
		queue<pair<int, int>> q; 
        int res = INT_MAX;
        q.push({ src, 0 });
        distance[src] = 0;
        while(q.size() > 0) {
        	auto it = q.front();
        	q.pop();
        	for (auto neighbour : graph[it.first]) {
        		if (distance[neighbour] > it.second + 1) {
        		    distance[neighbour] = it.second + 1;
        		    q.push({ neighbour, distance[neighbour] });
        		}
        	}
        }
        return distance[dest] == INT_MAX ? -1 : distance[dest];
    }
};


Tip: 
---
in above problem, you can store only 
    queue<int> q; // store only node in q. 
    for distance use the distance vector always.


https://www.naukri.com/code360/problems/shortest-path-in-an-unweighted-graph_981297?leftPanelTabValue=PROBLEM

the solution i solved is not good. we can solve this in simple way by storing parent as well.