# 2. Merge Sort

Split the array into halves, sort both halves, and merge them.

```cpp
void merge(vector<int>& nums, int low, int middle, int high) {
    vector<int> merged;
    int left = low;
    int right = middle + 1;

    while (left <= middle && right <= high) {
        if (nums[left] <= nums[right]) {
            merged.push_back(nums[left++]);
        } else {
            merged.push_back(nums[right++]);
        }
    }

    while (left <= middle) merged.push_back(nums[left++]);
    while (right <= high) merged.push_back(nums[right++]);

    for (int i = low; i <= high; ++i) {
        nums[i] = merged[i - low];
    }
}

void mergeSort(vector<int>& nums, int low, int high) {
    if (low >= high) return;

    int middle = low + (high - low) / 2;
    mergeSort(nums, low, middle);
    mergeSort(nums, middle + 1, high);
    merge(nums, low, middle, high);
}
```

Call it with:

```cpp
mergeSort(nums, 0, nums.size() - 1);
```

Time: `O(n log n)`; extra space: `O(n)`.

## Count inversions

An inversion is a pair where `i < j` but `nums[i] > nums[j]`.

During merging, when `nums[left] > nums[right]`, every remaining value from `left` through `middle` is also greater than `nums[right]`:

```cpp
count += middle - left + 1;
```

The same merge-sort idea is used for Reverse Pairs and Count of Smaller Numbers After Self.
