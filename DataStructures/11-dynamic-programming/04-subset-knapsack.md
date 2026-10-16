# 4. Subset, Knapsack, and Coin Change

These problems usually have two choices:

```text
take the current item
skip the current item
```

## 0/1 versus unbounded

| Type | How often can an item be used? | 1D loop direction |
|---|---:|---|
| 0/1 knapsack | Once | Target moves backward |
| Unbounded knapsack | Unlimited | Target moves forward |

The loop direction is extremely important.

## 0/1 subset sum

```cpp
bool canMakeTarget(vector<int>& nums, int target) {
    vector<bool> dp(target + 1, false);
    dp[0] = true;

    for (int number : nums) {
        for (int sum = target; sum >= number; --sum) {
            dp[sum] = dp[sum] || dp[sum - number];
        }
    }

    return dp[target];
}
```

Move backward so the same number is not reused during its iteration.

## Coin Change — minimum number of coins

Every coin can be used unlimited times, so amount moves forward.

```cpp
int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;

    for (int coin : coins) {
        for (int currentAmount = coin; currentAmount <= amount; ++currentAmount) {
            dp[currentAmount] = min(
                dp[currentAmount],
                1 + dp[currentAmount - coin]
            );
        }
    }

    return dp[amount] > amount ? -1 : dp[amount];
}
```

`amount + 1` safely represents an impossible value because no valid answer can require more than `amount` coins when coin value is at least 1.

## Coin Change II — number of combinations

```cpp
int change(int amount, vector<int>& coins) {
    vector<long long> dp(amount + 1, 0);
    dp[0] = 1;

    for (int coin : coins) {
        for (int currentAmount = coin; currentAmount <= amount; ++currentAmount) {
            dp[currentAmount] += dp[currentAmount - coin];
        }
    }

    return dp[amount];
}
```

Keeping coins in the outer loop counts combinations, not different orders of the same combination.

## Important transformations

| Problem | Transformation |
|---|---|
| Partition Equal Subset Sum | Find subset with sum `total / 2` |
| Minimum Subset Sum Difference | Find reachable sum closest to `total / 2` |
| Target Sum | Convert signs into a subset-count problem |
| Count Partitions with Difference | Convert difference into a subset target |
