# 3. Important Array Patterns

## Kadane's algorithm

Maximum sum of a contiguous subarray.

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        // At every index, start a new subarray
        // or extend the previous subarray.
        int currSum = 0;
        int bestSum = INT_MIN;

        for (int i = 0; i < nums.size(); i++) {
            currSum = max(currSum + nums[i], nums[i]);
            bestSum = max(currSum, bestSum);
        }

        return bestSum;
    }
};
```

At every index, either start a new subarray or extend the previous one.

## Sort 0s, 1s, and 2s

```cpp
void sortColors(vector<int>& nums) {
    int low = 0;
    int middle = 0;
    int high = nums.size() - 1;

    while (middle <= high) {
        if (nums[middle] == 0) {
            swap(nums[low++], nums[middle++]);
        } else if (nums[middle] == 1) {
            ++middle;
        } else {
            swap(nums[middle], nums[high--]);
        }
    }
}
```

```text
[0 ... low-1]       contains 0
[low ... middle-1]  contains 1
[high+1 ... n-1]    contains 2
```

## Majority element greater than `n / 2`

```cpp
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int count = 0;
        int candidate = 0;

        for (int i = 0; i < nums.size(); i++) {
            if (count == 0) {
                candidate = nums[i];
            }

            count = (candidate == nums[i] ? count + 1 : count - 1);
        }

        return candidate;
    }
};
```

If the problem does not guarantee a majority, count the candidate in a second pass.

## Next permutation — ⭐⭐⭐⭐⭐ Must revise

```cpp
class Solution {
public:
    void nextPermutation(vector<int>& nums) {
        int n = nums.size();
        int index = n - 2;

        // Find the first smaller number from the right.
        while (index >= 0 && nums[index] >= nums[index + 1]) {
            index--;
        }

        if (index >= 0) {
            // Find the smallest number larger than nums[index].
            int nextLarger = n - 1;

            while (nums[nextLarger] <= nums[index]) {
                nextLarger--;
            }

            swap(nums[index], nums[nextLarger]);
        }

        // Make the remaining part as small as possible.
        reverse(nums.begin() + index + 1, nums.end());
    }
};
```

### Algorithm

1. From the right, find the first index where `nums[index] < nums[index + 1]`.
2. If found, search from the right for the first number greater than `nums[index]`.
3. Swap these two numbers.
4. Reverse the array after `index` to make the remaining part smallest.

If the array is `[3, 2, 1]`, no smaller number is found. Reversing the complete array gives `[1, 2, 3]`.

### Why reversal is enough

The suffix is already in descending order. Descending is its largest arrangement; reversing it produces ascending order, its smallest arrangement.

### Complexity

```text
Time:  O(n)
Space: O(1)
```
