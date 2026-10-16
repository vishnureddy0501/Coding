# 3. Important Array Patterns

## Kadane's algorithm

Maximum sum of a contiguous subarray.

```cpp
int maxSubArray(vector<int>& nums) {
    int currentSum = nums[0];
    int bestSum = nums[0];

    for (int i = 1; i < nums.size(); ++i) {
        currentSum = max(nums[i], currentSum + nums[i]);
        bestSum = max(bestSum, currentSum);
    }

    return bestSum;
}
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
int majorityElement(vector<int>& nums) {
    int candidate = 0;
    int count = 0;

    for (int value : nums) {
        if (count == 0) candidate = value;
        count += value == candidate ? 1 : -1;
    }

    return candidate;
}
```

If the problem does not guarantee a majority, count the candidate in a second pass.

## Next permutation

```cpp
void nextPermutation(vector<int>& nums) {
    int breakpoint = nums.size() - 2;

    while (breakpoint >= 0 && nums[breakpoint] >= nums[breakpoint + 1]) {
        --breakpoint;
    }

    if (breakpoint >= 0) {
        int larger = nums.size() - 1;
        while (nums[larger] <= nums[breakpoint]) --larger;
        swap(nums[breakpoint], nums[larger]);
    }

    reverse(nums.begin() + breakpoint + 1, nums.end());
}
```

Steps: find breakpoint → swap with the next larger value → reverse the suffix.
