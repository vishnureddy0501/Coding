# 5. Matrix and Miscellaneous Patterns

## Pascal's Triangle row

Generate a row without repeatedly calculating factorials.

```cpp
vector<long long> generateRow(int rowNumber) {
    vector<long long> row;
    long long value = 1;
    row.push_back(value);

    for (int column = 1; column < rowNumber; ++column) {
        value = value * (rowNumber - column) / column;
        row.push_back(value);
    }

    return row;
}
```

## Matrix patterns to know

- Set Matrix Zeroes: use the first row and column as markers.
- Rotate Image: transpose, then reverse every row.
- Spiral Matrix: maintain top, right, bottom, and left boundaries.
- Search a sorted matrix: use binary search or start from the top-right corner.
- Game of Life: encode old and new states inside the same cell.

## Count inversions and reverse pairs

These are merge-sort problems. See [Merge Sort](../02-sorting/02-merge-sort.md).

## Repeating and missing number

Common approaches:

1. frequency array;
2. mathematical sum and sum of squares;
3. XOR partitioning.

Use `long long` for sum and square calculations.
