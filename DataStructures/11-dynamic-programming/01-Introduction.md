When is a DP Problem?
---------------------
1. count the number of ways
2. there are different ways to do a problems. find the minimum / maximum result.
3. trying all possible ways.

44. Wildcard Matching
494. Target Sum (2 approaches: Using recursion, Using dynamic programming)
983. Minimum Cost For Tickets
62. Unique Paths (doing this using DP is not optimal. We has more optimal than dp. which i have to find & learn)
1463. Cherry Pickup II
2035. Partition Array Into Two Arrays to Minimize Sum Difference (tried method not working because of constraints)


How to solve a DP problem:
--------------------------
1. Write the recursion (express the problem in terms of index / state).
2. Memoization: store results in dp[] (top-down).
3. Tabulation: fill dp[] bottom-up, base cases first.
4. Space optimization: keep only prev / curr rows (02-SpaceOptimization.md).

Standard patterns (study in this order):
    1D        : Climbing Stairs, Frog Jump, House Robber
    2D grid   : Unique Paths, Minimum Path Sum, Triangle, Cherry Pickup
    Subsets   : Subset Sum, Partition Equal Subset, Count Subsets with Sum K, 0/1 Knapsack,
                Coin Change (unbounded), Target Sum
    Strings   : LCS, Longest Palindromic Subsequence, Edit Distance, Wildcard Matching
    Stocks    : Best Time to Buy and Sell Stock I - IV, with cooldown / fee
    LIS       : Longest Increasing Subsequence, Largest Divisible Subset, Number of LIS
    Partition : Matrix Chain Multiplication, Burst Balloons, Min Score Triangulation of Polygon

Naukari -> count-subsets-with-sum-k
