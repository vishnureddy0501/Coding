# Bipartite Graph
-----------------
A graph is bipartite if adjacent nodes can be colored using two different colors.

- Every graph without a cycle is bipartite.
- A graph containing an odd-length cycle is not bipartite.
- A graph containing only even-length cycles can still be bipartite.



class Solution {
  public:
  bool isSafe (vector<int>& colors, vector<vector<int>>& v, int index) {
      queue<int> q;
      q.push(index);
      colors[index] = 0;
      while(q.size() > 0) {
          auto it = q.front();
          q.pop();
          for (auto neighbour: v[it]) {
              if (colors[neighbour] == -1) {
                  colors[neighbour] = (colors[it] == 0 ? 1: 0);
                  q.push(neighbour);
              } else {
                  if (colors[neighbour] == colors[it]) return false;
              }
          }
      }
      return true;
  }
    bool isBipartite(int n, vector<vector<int>> &edges) {
        vector<vector<int>> v(n);
        for (int i = 0; i < edges.size(); i++) {
            v[edges[i][0]].push_back(edges[i][1]);
            v[edges[i][1]].push_back(edges[i][0]);
        }
        vector<int> colors(n, -1);
        for (int i = 0; i<n; i++) {
            if (colors[i] == -1) {
               if (!isSafe(colors, v, i)) return false;
            }
        }
        return true;
    }
};
