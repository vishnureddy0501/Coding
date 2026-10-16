# 3. Permutations and Duplicates

## Permutations I — ⭐⭐⭐⭐⭐ Must revise

[LeetCode 46: Permutations](https://leetcode.com/problems/permutations/)

A permutation uses every number, and order matters.

```text
[1, 2] -> [1, 2] and [2, 1]
```

Use a map to remember which number is already present in the current permutation.

```cpp
class Solution {
public:
    void combineHelper(
        vector<vector<int>>& res,
        vector<int>& current,
        vector<int>& nums,
        unordered_map<int, int>& visited
    ) {
        if (current.size() == nums.size()) {
            res.push_back(current);
            return;
        }

        for (int i = 0; i < nums.size(); i++) {
            if (visited[nums[i]]) continue;

            current.push_back(nums[i]);
            visited[nums[i]] = 1;

            combineHelper(res, current, nums, visited);

            current.pop_back();
            visited[nums[i]] = 0;
        }
    }

    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> res;
        vector<int> current;
        unordered_map<int, int> visited;

        combineHelper(res, current, nums, visited);
        return res;
    }
};
```

This map-based solution works for **Permutations I** because the input values are distinct.

```text
Choose number -> mark used -> recurse -> remove number -> mark unused
```

## Permutations II — ⭐⭐⭐⭐⭐ Must revise

[LeetCode 47: Permutations II](https://leetcode.com/problems/permutations-ii/)

For **Permutations II**, duplicate values are allowed. The map-by-value solution above cannot distinguish their separate positions.

Use an index-based `visited` array, sort first, and add this check:

```cpp
if (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1]) {
    continue;
}
```

Complete choice check:

```cpp
if (visited[i]) continue;

if (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1]) {
    continue;
}
```

## Why this duplicate condition?

Consider sorted input `[1a, 1b, 2]`. Here, `1a` and `1b` have the same value but different indices.

```cpp
i > 0
```

The current number has a previous number.

```cpp
nums[i] == nums[i - 1]
```

The current and previous numbers are duplicates.

```cpp
!visited[i - 1]
```

The previous duplicate is not used in the current path. Choosing the current duplicate now would create the same permutation that starts with the previous duplicate, so we skip it.

However, if `visited[i - 1]` is true, the previous duplicate is already part of the current permutation. The current duplicate is then allowed:

```text
[]          -> choose 1a; skip starting with 1b
[1a]        -> choosing 1b is allowed
[1a, 1b]   -> valid use of both duplicate values
```

In short: equal values must be selected from left to right. This prevents duplicate permutations.

## Combination versus permutation

```text
Combination: order does not matter -> move forward using start index
Permutation: order matters         -> try every unused index
```
