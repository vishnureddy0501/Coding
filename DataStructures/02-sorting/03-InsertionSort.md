# Insertion Sort

Keep the left portion sorted and insert the current element into its correct position.

```cpp
for (int i = 1; i < nums.size(); i++) {
    int value = nums[i];
    int j = i - 1;

    while (j >= 0 && nums[j] > value) {
        nums[j + 1] = nums[j];
        --j;
    }
    nums[j + 1] = value;
}
```

Time: `O(n²)` normally and `O(n)` for an already sorted array. Space: `O(1)`.
