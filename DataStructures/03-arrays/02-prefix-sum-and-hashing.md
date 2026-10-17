# 2. Prefix Sum and Hashing

## Main prefix-sum idea

```text
prefix[i] = sum of elements from 0 to i

sum(left ... right) = prefix[right] - prefix[left - 1]
```

## Count subarrays with sum `k` — ⭐⭐⭐⭐⭐ Must revise

If the current prefix sum is `prefix`, we need an earlier prefix equal to `prefix - k`.

```cpp
int subarraySum(vector<int>& nums, int k) {
    unordered_map<long long, int> frequency;
    frequency[0] = 1;

    long long prefix = 0;
    int count = 0;

    for (int value : nums) {
        prefix += value;
        count += frequency[prefix - k];
        ++frequency[prefix];
    }

    return count;
}
```

This works with positive, zero, and negative values.

## Longest subarray with sum `k`

Store only the first index of each prefix sum to maximize length.

```cpp
int longestSubarrayWithSumK(vector<int> nums, long long k) {
    unordered_map<long long, long long> m;
    int n = nums.size();
    long long res = 0;
    long long sum = 0;

    for (long long i = 0; i < n; i++) {
        sum = sum + nums[i];

        if (sum == k) {
            res = max(res, i + 1);
        }

        if (m.find(sum - k) != m.end()) {
            res = max(res, i - m[sum - k]);
        }

        if (m.find(sum) == m.end()) {
            m[sum] = i;
        }
    }

    return res;
}
```

## Count subarrays with XOR `k`

```cpp
int subarraysWithXor(vector<int>& nums, int k) {
    unordered_map<int, int> frequency;
    frequency[0] = 1;

    int prefixXor = 0;
    int count = 0;

    for (int value : nums) {
        prefixXor ^= value;
        count += frequency[prefixXor ^ k];
        ++frequency[prefixXor];
    }

    return count;
}
```

Remember:

```text
previousPrefix XOR k = currentPrefix
previousPrefix = currentPrefix XOR k
```
