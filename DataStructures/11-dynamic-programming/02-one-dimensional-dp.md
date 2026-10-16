# 2. One-Dimensional DP

Use 1D DP when the answer at an index depends on a few earlier indices.

## House Robber

At every house, either take it and skip the previous house, or skip it.

```cpp
int rob(vector<int>& nums) {
    int previousTwo = 0;
    int previousOne = 0;

    for (int money : nums) {
        int take = money + previousTwo;
        int skip = previousOne;
        int current = max(take, skip);

        previousTwo = previousOne;
        previousOne = current;
    }

    return previousOne;
}
```

```text
State:      maximum money up to the current house
Transition: current = max(money + previousTwo, previousOne)
Time:       O(n)
Space:      O(1)
```

## Maximum sum of non-adjacent elements

This is the same pattern as House Robber.

## House Robber II

The first and last houses are adjacent because the houses form a circle.

```text
Answer = max(
    rob houses from 0 to n - 2,
    rob houses from 1 to n - 1
)
```

## Other important 1D problems

- Climbing Stairs
- Min Cost Climbing Stairs
- Decode Ways
- Maximum Product Subarray
- Word Break
