# 7. Important Interview Problems

Solve in this order. The first three levels cover the most common interview patterns.

## Level 1 — foundations

| # | Problem | Pattern |
|---:|---|---|
| 1 | LeetCode 70 — Climbing Stairs | Basic 1D DP |
| 2 | LeetCode 198 — House Robber | Take/skip |
| 3 | LeetCode 213 — House Robber II | Circular 1D DP |
| 4 | LeetCode 746 — Min Cost Climbing Stairs | Minimum 1D DP |
| 5 | LeetCode 91 — Decode Ways | Counting ways |

## Level 2 — grids and subsets

| # | Problem | Pattern |
|---:|---|---|
| 6 | LeetCode 62 — Unique Paths | Grid counting |
| 7 | LeetCode 64 — Minimum Path Sum | Grid minimum |
| 8 | LeetCode 120 — Triangle | Variable-width grid |
| 9 | LeetCode 931 — Minimum Falling Path Sum | Grid transitions |
| 10 | LeetCode 416 — Partition Equal Subset Sum | 0/1 subset sum |
| 11 | LeetCode 494 — Target Sum | Subset transformation |
| 12 | LeetCode 322 — Coin Change | Unbounded minimum |
| 13 | LeetCode 518 — Coin Change II | Unbounded counting |
| 14 | Count Subsets with Sum K | 0/1 subset counting |
| 15 | 0/1 Knapsack | Classic take/skip |

## Level 3 — strings and sequences

| # | Problem | Pattern |
|---:|---|---|
| 16 | LeetCode 1143 — Longest Common Subsequence | Two-string DP |
| 17 | LeetCode 516 — Longest Palindromic Subsequence | LCS transformation |
| 18 | LeetCode 72 — Edit Distance | Insert/delete/replace |
| 19 | LeetCode 115 — Distinct Subsequences | String counting |
| 20 | LeetCode 44 — Wildcard Matching | String matching |
| 21 | LeetCode 300 — Longest Increasing Subsequence | LIS |
| 22 | LeetCode 673 — Number of LIS | Count optimal sequences |
| 23 | LeetCode 139 — Word Break | Prefix partitioning |

## Level 4 — stocks and advanced partitioning

| # | Problem | Pattern |
|---:|---|---|
| 24 | LeetCode 122 — Best Time to Buy and Sell Stock II | Buy/sell state |
| 25 | LeetCode 309 — Stock with Cooldown | Extra state |
| 26 | LeetCode 714 — Stock with Transaction Fee | Buy/sell state |
| 27 | Matrix Chain Multiplication | Partition DP |
| 28 | LeetCode 312 — Burst Balloons | Interval DP |
| 29 | LeetCode 1039 — Minimum Score Triangulation | Interval DP |
| 30 | LeetCode 983 — Minimum Cost for Tickets | Choice by day/index |
| 31 | LeetCode 1463 — Cherry Pickup II | Two-agent grid DP |

## Minimum revision set

If time is limited, repeatedly solve these ten:

1. House Robber
2. Unique Paths
3. Minimum Path Sum
4. Partition Equal Subset Sum
5. Coin Change
6. Target Sum
7. Longest Common Subsequence
8. Edit Distance
9. Longest Increasing Subsequence
10. Stock II

## Revision checklist

For every problem, write:

```text
State:
Choices:
Transition:
Base cases:
Iteration order:
Time and space:
```

First make memoization work. Then convert it to tabulation. Optimize space only when the dependency is clear.
