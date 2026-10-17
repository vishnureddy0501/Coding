# 5. Matrix and Miscellaneous Patterns

## Pascal's Triangle I

[LeetCode 118: Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/)

```cpp
class Solution {
public:
    vector<vector<int>> generate(int numRows) {
        vector<vector<int>> res;

        for (int row = 0; row < numRows; row++) {
            vector<int> current(row + 1, 1);

            for (int col = 1; col < row; col++) {
                current[col] =
                    res[row - 1][col - 1] +
                    res[row - 1][col];
            }

            res.push_back(current);
        }

        return res;
    }
};
```

## Pascal's Triangle II

[LeetCode 119: Pascal's Triangle II](https://leetcode.com/problems/pascals-triangle-ii/)

> Use the same previous-row logic. You do not need to learn the combination formula.

```cpp
class Solution {
public:
    vector<int> getRow(int rowIndex) {
        vector<int> previous;

        for (int row = 0; row <= rowIndex; row++) {
            vector<int> current(row + 1, 1);

            for (int col = 1; col < row; col++) {
                current[col] =
                    previous[col - 1] +
                    previous[col];
            }

            previous = current;
        }

        return previous;
    }
};
```

## Matrix patterns to know

- Set Matrix Zeroes: use the first row and column as markers.
- Rotate Image: transpose, then reverse every row.
- Spiral Matrix: maintain top, right, bottom, and left boundaries.
- Search a sorted matrix: use binary search or start from the top-right corner.
- Game of Life: encode old and new states inside the same cell.

## Count inversions and reverse pairs

These are merge-sort problems. See [Merge Sort](../02-sorting/01-merge-sort.md).

## Repeating and missing number

Common approaches:

1. frequency array;
2. mathematical sum and sum of squares;
3. XOR partitioning.

Use `long long` for sum and square calculations.
