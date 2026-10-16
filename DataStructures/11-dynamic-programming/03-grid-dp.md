# 3. Grid DP

Most grid problems use this state:

```text
dp[row][column] = answer for reaching or starting from this cell
```

## Unique Paths

You can reach a cell from the top or left.

```cpp
int uniquePaths(int rows, int columns) {
    vector<int> dp(columns, 1);

    for (int row = 1; row < rows; ++row) {
        for (int column = 1; column < columns; ++column) {
            dp[column] = dp[column] + dp[column - 1];
        }
    }

    return dp[columns - 1];
}
```

```text
dp[column]     = paths from the top
dp[column - 1] = paths from the left
```

Time: `O(rows × columns)`; space: `O(columns)`.

## Minimum Path Sum

```cpp
int minPathSum(vector<vector<int>>& grid) {
    int rows = grid.size();
    int columns = grid[0].size();
    vector<int> dp(columns, INT_MAX);
    dp[0] = 0;

    for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
            int fromTop = dp[column];
            int fromLeft = column > 0 ? dp[column - 1] : INT_MAX;
            dp[column] = grid[row][column] + min(fromTop, fromLeft);
        }
    }

    return dp[columns - 1];
}
```

## Grid checklist

- What movements are allowed?
- Is the answer counting paths, minimizing cost, or maximizing value?
- Are any cells blocked?
- Does the state need another dimension, such as remaining health or two robot columns?
