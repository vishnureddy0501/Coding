# Dynamic Programming

Dynamic programming saves answers to repeated subproblems instead of calculating them again.

## Study order

1. [How to solve DP problems](01-how-to-solve-dp.md)
2. [One-dimensional DP](02-one-dimensional-dp.md)
3. [Grid DP](03-grid-dp.md)
4. [Subset, knapsack, and coin change](04-subset-knapsack.md)
5. [String DP](05-string-dp.md)
6. [Space optimization](06-space-optimization.md)
7. [Important interview problems](07-important-problems.md)

## Main patterns

| Pattern | Typical state | Examples |
|---|---|---|
| 1D DP | `dp[index]` | Climbing Stairs, House Robber |
| Grid DP | `dp[row][column]` | Unique Paths, Minimum Path Sum |
| Subset/knapsack | `dp[index][target]` | Subset Sum, Coin Change |
| String DP | `dp[i][j]` | LCS, Edit Distance |
| Stock DP | `dp[day][canBuy]` | Buy and Sell Stock II–IV |
| LIS | `dp[index]` | Longest Increasing Subsequence |
| Partition DP | `dp[left][right]` | Matrix Chain, Burst Balloons |

Do not memorize complete solutions. Memorize how to define the state, transition, and base case.
