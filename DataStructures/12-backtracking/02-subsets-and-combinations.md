# 2. Subsets and Combinations

For a step-by-step recursion tree, read [Subsets explained](02-subsets-explained.md).

## Subsets: loop-based solution

```cpp
class Solution {
public:
    void generateAll(
        vector<vector<int>>& res,
        vector<int>& nums,
        vector<int>& current,
        int index
    ) {
        res.push_back(current);

        for (int i = index; i < nums.size(); i++) {
            current.push_back(nums[i]);
            generateAll(res, nums, current, i + 1);
            current.pop_back();
        }
    }

    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> res;
        vector<int> current;

        generateAll(res, nums, current, 0);
        return res;
    }
};
```

## Subsets: pick or do not pick

For every value, make two choices:

```text
pick it
do not pick it
```

```cpp
void findSubsets(
    int index,
    vector<int>& nums,
    vector<int>& current,
    vector<vector<int>>& answer
) {
    if (index == nums.size()) {
        answer.push_back(current);
        return;
    }

    current.push_back(nums[index]);
    findSubsets(index + 1, nums, current, answer);
    current.pop_back();

    findSubsets(index + 1, nums, current, answer);
}
```

## Combinations: choose the next value

Use a loop when order does not matter.

```cpp
void findCombinations(
    int start,
    int n,
    int k,
    vector<int>& current,
    vector<vector<int>>& answer
) {
    if (current.size() == k) {
        answer.push_back(current);
        return;
    }

    for (int value = start; value <= n; value++) {
        current.push_back(value);
        findCombinations(value + 1, n, k, current, answer);
        current.pop_back();
    }
}
```

`value + 1` prevents selecting the same value again.

## Combination Sum

If the same value may be reused, recurse using the same index:

```cpp
solve(index, remaining - nums[index]);
```

## Combination Sum II — ⭐⭐⭐⭐⭐ Must revise

> **Revision note:** Study only this pick/not-pick recursive solution. Skip the for-loop solution.

```cpp
class Solution {
public:
    void generateCombinations(
        vector<vector<int>>& result,
        vector<int>& current,
        vector<int>& nums,
        int target,
        int index
    ) {
        if (target == 0) {
            result.push_back(current);
            return;
        }

        if (target < 0 || index >= nums.size()) {
            return;
        }

        // Pick the current number
        current.push_back(nums[index]);

        generateCombinations(
            result,
            current,
            nums,
            target - nums[index],
            index + 1
        );

        current.pop_back();

        // Do not pick it; skip all copies of the same number
        int nextIndex = index + 1;

        while (
            nextIndex < nums.size() &&
            nums[nextIndex] == nums[index]
        ) {
            nextIndex++;
        }

        generateCombinations(
            result,
            current,
            nums,
            target,
            nextIndex
        );
    }

    vector<vector<int>> combinationSum2(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());

        vector<vector<int>> result;
        vector<int> current;

        generateCombinations(result, current, nums, target, 0);
        return result;
    }
};
```

Why sort? Duplicate values come together.

Why skip duplicates only in the **do not pick** call? Once we decide not to use this value at the current position, trying its identical copies would produce the same combinations.

The same duplicate-skipping idea is used in **Subsets II**.
