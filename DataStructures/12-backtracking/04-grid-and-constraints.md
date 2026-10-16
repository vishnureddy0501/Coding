# 4. Grid and Constraint Problems

## Word Search pattern

Choose a neighboring cell, explore it, and restore it afterward.

```cpp
bool search(
    int row,
    int col,
    int index,
    vector<vector<char>>& board,
    string& word
) {
    if (index == word.size()) return true;

    int rows = board.size();
    int cols = board[0].size();

    if (row < 0 || row >= rows || col < 0 || col >= cols) {
        return false;
    }

    if (board[row][col] != word[index]) return false;

    char original = board[row][col];
    board[row][col] = '#';

    bool found =
        search(row + 1, col, index + 1, board, word) ||
        search(row - 1, col, index + 1, board, word) ||
        search(row, col + 1, index + 1, board, word) ||
        search(row, col - 1, index + 1, board, word);

    board[row][col] = original;
    return found;
}
```

Temporarily changing the cell prevents using it twice in the same path.

## N-Queens idea

Complete code: [N-Queens](04-n-queens.md)

Place one queen in each row.

Before placing it, check that its:

- Column is unused.
- Left diagonal is unused.
- Right diagonal is unused.

```text
column index        = col
left diagonal       = row - col + n - 1
right diagonal      = row + col
```

Use arrays for these checks instead of scanning the board every time.

## Sudoku idea

1. Find an empty cell.
2. Try digits `1` to `9`.
3. Continue only if row, column, and box rules are valid.
4. If the next recursion fails, make the cell empty again.

```text
choose digit -> solve remaining board -> undo if it fails
```

## Return early or collect all?

- Word Search and Sudoku usually need one valid solution: return `true` early.
- N-Queens may ask for every solution: store the answer and continue searching.
