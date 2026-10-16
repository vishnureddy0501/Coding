# 3. Count Subarrays with an Exact Condition

Exact conditions are often difficult to maintain directly. Convert them into two at-most conditions:

```text
exactly(k) = atMost(k) - atMost(k - 1)
```

## Binary subarrays with sum

This works because the array contains only `0` and `1`.

```cpp
long long atMostSum(vector<int>& nums, int goal) {
    if (goal < 0) return 0;

    int left = 0;
    int sum = 0;
    long long count = 0;

    for (int right = 0; right < nums.size(); ++right) {
        sum += nums[right];

        while (sum > goal) {
            sum -= nums[left++];
        }

        count += right - left + 1;
    }

    return count;
}

long long numSubarraysWithSum(vector<int>& nums, int goal) {
    return atMostSum(nums, goal) - atMostSum(nums, goal - 1);
}
```

## Exactly `k` odd numbers

Treat each odd number as `1` and each even number as `0`, then use the same at-most-sum pattern.

## Exactly `k` distinct integers

```cpp
long long atMostKDistinct(vector<int>& nums, int k) {
    if (k < 0) return 0;

    unordered_map<int, int> frequency;
    int left = 0;
    long long count = 0;

    for (int right = 0; right < nums.size(); ++right) {
        ++frequency[nums[right]];

        while (frequency.size() > k) {
            --frequency[nums[left]];
            if (frequency[nums[left]] == 0) frequency.erase(nums[left]);
            ++left;
        }

        count += right - left + 1;
    }

    return count;
}

long long subarraysWithKDistinct(vector<int>& nums, int k) {
    return atMostKDistinct(nums, k) - atMostKDistinct(nums, k - 1);
}
```

For subarray sum with negative numbers, this technique is invalid. Use prefix sum with a hash map.
