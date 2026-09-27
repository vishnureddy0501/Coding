# Shortest Path in a Binary Maze

[Practice problem](https://www.naukri.com/code360/problems/shortest-path-in-a-binary-maze_893065)

Problem: grid of 0/1. Move only through cells with 1 (up/down/left/right).
Find the minimum steps from src to dest, or -1 if not reachable.

Idea:
    Every move costs 1, so plain BFS already gives the shortest path.
    (Striver solves it with "Dijkstra using a queue". With unit weights that is exactly this BFS.)

int shortestPathBinaryMatrix(vector<vector<int>> &matrix, pair<int, int> src, pair<int, int> dest) {
    int n = matrix.size(), m = matrix[0].size();
    if (matrix[src.first][src.second] == 0 || matrix[dest.first][dest.second] == 0) return -1;
    if (src == dest) return 0;

    vector<vector<int>> dist(n, vector<int>(m, INT_MAX));
    queue<pair<int, int>> q;
    q.push(src);
    dist[src.first][src.second] = 0;

    int dr[] = {-1, 0, 1, 0};
    int dc[] = {0, 1, 0, -1};
    while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr >= 0 && nr < n && nc >= 0 && nc < m && matrix[nr][nc] == 1
                && dist[nr][nc] > dist[r][c] + 1) {
                dist[nr][nc] = dist[r][c] + 1;
                if (make_pair(nr, nc) == dest) return dist[nr][nc];
                q.push({nr, nc});
            }
        }
    }
    return -1;
}

Note: LeetCode 1091 (Shortest Path in Binary Matrix) is the same idea but allows 8 directions,
the path goes through 0 cells, and the answer counts cells (not steps).
