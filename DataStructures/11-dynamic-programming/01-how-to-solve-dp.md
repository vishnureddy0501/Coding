# 1. How to Solve DP Problems

## When should you think about DP?

A problem often needs DP when:

- it asks for the number of ways;
- it asks for a minimum or maximum result after making choices;
- the recursive solution tries multiple choices;
- the same state is calculated repeatedly.

DP requires **overlapping subproblems** and an **optimal substructure**. A maximize/minimize question is not automatically DP.

## The five-step method

### 1. Define the state

Write one sentence explaining the meaning of `dp`.

```text
dp[i] = best answer using elements from index 0 to i
```

For two changing values:

```text
dp[i][target] = whether target can be formed using elements 0 to i
```

### 2. Write the choices and transition

Example for House Robber:

```text
skip house i: dp[i - 1]
rob house i:  nums[i] + dp[i - 2]

dp[i] = max(skip, rob)
```

### 3. Write base cases

Base cases must represent the smallest valid states.

```text
dp[0] = nums[0]
dp[1] = max(nums[0], nums[1])
```

### 4. Choose an implementation

```text
Recursion   → easiest way to derive the relation
Memoization → recursion + cache
Tabulation  → build answers iteratively
Optimization → keep only states still needed
```

### 5. Calculate complexity

```text
Time = number of states × work per state
Space = DP table + recursion stack
```

## Memoization template

```cpp
int solve(int index, vector<int>& nums, vector<int>& dp) {
    if (index < 0) return 0;
    if (dp[index] != -1) return dp[index];

    int take = nums[index] + solve(index - 2, nums, dp);
    int skip = solve(index - 1, nums, dp);

    return dp[index] = max(take, skip);
}
```

## Important interview rule

Explain these before writing code:

1. What does the state mean?
2. What choices are available?
3. What is the recurrence?
4. What are the base cases?
5. What are the time and space complexities?

If you cannot explain the state in one sentence, the DP is probably not clear yet.
