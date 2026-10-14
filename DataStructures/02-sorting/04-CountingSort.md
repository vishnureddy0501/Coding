# Counting Sort

Useful when values are non-negative and their maximum value `k` is reasonably small.

```cpp
vector<int> countingSort(const vector<int>& nums, int maxValue) {
    vector<int> frequency(maxValue + 1, 0);
    vector<int> result;
    result.reserve(nums.size());

    for (int value : nums) ++frequency[value];

    for (int value = 0; value <= maxValue; ++value) {
        while (frequency[value]-- > 0) result.push_back(value);
    }

    return result;
}
```

Time: `O(n + k)`; space: `O(k)`.
