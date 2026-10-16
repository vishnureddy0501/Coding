# 1. Core Templates

## When should you use sliding window?

Think about it when:

- the problem asks about a contiguous subarray or substring;
- the right boundary can expand one step at a time;
- moving the left boundary can restore a valid condition.

Sliding window usually requires a condition that behaves predictably when the window grows or shrinks. For arbitrary negative numbers, sum-based windows often do not work; use prefix sum and hashing instead.

## Fixed-size window

```cpp
long long maximumWindowSum(vector<int>& nums, int k) {
    long long windowSum = 0;

    for (int i = 0; i < k; ++i) {
        windowSum += nums[i];
    }

    long long answer = windowSum;

    for (int right = k; right < nums.size(); ++right) {
        windowSum += nums[right];
        windowSum -= nums[right - k];
        answer = max(answer, windowSum);
    }

    return answer;
}
```

## Longest valid window

```cpp
int left = 0;
int answer = 0;

for (int right = 0; right < n; ++right) {
    add(nums[right]);

    while (windowIsInvalid()) {
        remove(nums[left]);
        ++left;
    }

    answer = max(answer, right - left + 1);
}
```

## Count valid windows

After shrinking until the window is valid:

```cpp
count += right - left + 1;
```

Why? Every subarray ending at `right` and starting at any index from `left` through `right` is valid.

## Window length

For inclusive boundaries:

```cpp
length = right - left + 1;
```
