# N-Queens — ⭐⭐⭐⭐⭐ Must revise

[LeetCode 51: N-Queens](https://leetcode.com/problems/n-queens/)

Place exactly one queen in every row.

```text
Current row
   -> try every column
   -> place queen if safe
   -> solve next row
   -> remove queen
```

## Simple code

```cpp
class Solution {
public:
    bool checkValidity(
        vector<string>& board,
        int row,
        int col,
        int n
    ) {
        // Check column above
        for (int i = 0; i < row; i++) {
            if (board[i][col] == 'Q') {
                return false;
            }
        }

        // Check top-left diagonal
        for (int i = row - 1, j = col - 1;
             i >= 0 && j >= 0;
             i--, j--) {
            if (board[i][j] == 'Q') {
                return false;
            }
        }

        // Check top-right diagonal
        for (int i = row - 1, j = col + 1;
             i >= 0 && j < n;
             i--, j++) {
            if (board[i][j] == 'Q') {
                return false;
            }
        }

        return true;
    }

    void solve(
        vector<vector<string>>& result,
        vector<string>& board,
        int row,
        int n
    ) {
        if (row == n) {
            result.push_back(board);
            return;
        }

        for (int col = 0; col < n; col++) {
            if (checkValidity(board, row, col, n)) {
                board[row][col] = 'Q';

                solve(result, board, row + 1, n);

                board[row][col] = '.';
            }
        }
    }

    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> result;
        vector<string> board(n, string(n, '.'));

        solve(result, board, 0, n);
        return result;
    }
};
```

## Why check only above?

Queens are placed from top to bottom. Rows below the current row are still empty.

```text
Previous rows -> may contain queens
Current row   -> placing now
Future rows   -> empty
```

The backtracking step is:

```cpp
board[row][col] = 'Q';
solve(result, board, row + 1, n);
board[row][col] = '.';
```

