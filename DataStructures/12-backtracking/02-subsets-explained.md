# Subsets — How Backtracking Works

[LeetCode 78: Subsets](https://leetcode.com/problems/subsets/)

For:

```text
nums = [1, 2, 3]
```

We need:

```text
[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]
```

The main idea is:

```text
Add a number -> explore answers containing it -> remove it -> try another number
```

That removal is backtracking.

---

## Approach 1: For-loop solution

```cpp
class Solution {
public:
    void generateAll(
        vector<vector<int>>& result,
        vector<int>& nums,
        vector<int>& current,
        int start
    ) {
        result.push_back(current);

        for (int i = start; i < nums.size(); i++) {
            current.push_back(nums[i]);
            generateAll(result, nums, current, i + 1);
            current.pop_back();
        }
    }

    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> current;

        generateAll(result, nums, current, 0);
        return result;
    }
};
```

## What does `start` mean?

`start` tells us where the next number can be selected.

```text
start = 0 -> choose 1, 2, or 3
start = 1 -> choose 2 or 3
start = 2 -> choose only 3
start = 3 -> nothing left
```

We use `i + 1` so the same number is not selected again.

## Recursion diagram

Every box is a valid subset, so it is immediately added to `result`.

```text
                      []
             /         |         \
           [1]        [2]        [3]
          /   \         \
       [1,2] [1,3]     [2,3]
         /
    [1,2,3]
```

The traversal order is:

```text
[] -> [1] -> [1,2] -> [1,2,3]
   -> [1,3] -> [2] -> [2,3] -> [3]
```

## Important backtracking step

Consider this part:

```cpp
current.push_back(nums[i]);
generateAll(result, nums, current, i + 1);
current.pop_back();
```

When exploring `[1,2]`:

```text
current = [1]

choose 2       -> [1,2]
explore deeper -> [1,2,3]
remove 2       -> [1]
choose 3       -> [1,3]
```

Without `pop_back()`, the next choice would incorrectly start from `[1,2]` instead of `[1]`.

## Why add the answer at the beginning?

In this approach, every `current` value is a valid subset:

```text
[] is valid
[1] is valid
[1,2] is valid
```

Therefore, we store it as soon as the function starts:

```cpp
result.push_back(current);
```

---

## Approach 2: Pick or do not pick

At every index, make exactly two choices:

```text
Pick nums[index]
Do not pick nums[index]
```

```cpp
class Solution {
public:
    void generateAll(
        int index,
        vector<int>& nums,
        vector<int>& current,
        vector<vector<int>>& result
    ) {
        if (index == nums.size()) {
            result.push_back(current);
            return;
        }

        // Pick nums[index]
        current.push_back(nums[index]);
        generateAll(index + 1, nums, current, result);
        current.pop_back();

        // Do not pick nums[index]
        generateAll(index + 1, nums, current, result);
    }

    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> current;

        generateAll(0, nums, current, result);
        return result;
    }
};
```

## Recursion diagram

```text
                              []
                    pick 1 /      \ skip 1
                         [1]       []
                pick 2 /  \       /  \ skip 2
                    [1,2] [1]    [2]  []
                   /  \   / \    / \  / \
             [1,2,3][1,2][1,3][1][2,3][2][3][]
```

Only the bottom level contains complete decisions for all three numbers. Therefore, this approach stores the answer only when:

```cpp
index == nums.size()
```

---

## Difference between the approaches

| For-loop approach | Pick/not-pick approach |
|---|---|
| Every call represents a valid subset | Every level makes a decision for one number |
| Store the answer at the start | Store the answer at the final level |
| Loop chooses the next available number | Two recursive calls: pick and skip |
| Usually easier for combinations and duplicates | Often easiest for understanding recursion |

Both generate all `2^n` subsets.

## The crux

```text
current stores the choices made on the current path.

push_back() adds one choice.
recursive call explores everything with that choice.
pop_back() removes it so another choice can be tried.
```

