# 6. Space Optimization

Optimize space only after the normal DP solution is correct.

## When is optimization possible?

If row `i` depends only on row `i - 1`, the complete 2D table is unnecessary.

```cpp
vector<int> previous(columns, 0);

for (int row = 0; row < rows; ++row) {
    vector<int> current(columns, 0);

    for (int column = 0; column < columns; ++column) {
        current[column] = /* use previous and current */;
    }

    previous = current;
}
```

Space changes from `O(rows × columns)` to `O(columns)`.

## When can two variables be used?

If the current state depends only on the previous one or two states:

```cpp
int previousTwo = 0;
int previousOne = 1;

for (int i = 2; i <= n; ++i) {
    int current = previousOne + previousTwo;
    previousTwo = previousOne;
    previousOne = current;
}
```

## Important warning

Updating a 1D array can overwrite a value that is still needed.

- 0/1 knapsack: iterate target backward.
- Unbounded knapsack: iterate target forward.
- Grid DP: decide whether `dp[column]` means the old top value or newly updated current-row value.

If you need to reconstruct the chosen path or print an LCS, keep the full table unless you use a more advanced reconstruction method.
