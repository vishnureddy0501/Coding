# 4. Counting Sort

Use counting sort when integer values lie inside a small known range.

```cpp
vector<int> countingSort(const vector<int>& nums, int maximumValue) {
    vector<int> frequency(maximumValue + 1, 0);

    for (int value : nums) {
        ++frequency[value];
    }

    vector<int> result;
    result.reserve(nums.size());

    for (int value = 0; value <= maximumValue; ++value) {
        while (frequency[value] > 0) {
            result.push_back(value);
            --frequency[value];
        }
    }

    return result;
}
```

Time: `O(n + k)`; extra space: `O(k)`, where `k` is the value range.

Do not use it when the range is extremely large compared with the number of elements.
