# Quick Sort — Optional

Choose a pivot, place smaller values on its left and larger values on its right, then recursively sort both portions.

```cpp
int partition(vector<int>& nums, int low, int high) {
    int pivot = nums[low];
    int left = low;
    int right = high;

    while (left < right) {
        while (left < high && nums[left] <= pivot) ++left;
        while (right > low && nums[right] > pivot) --right;

        if (left < right) swap(nums[left], nums[right]);
    }

    swap(nums[low], nums[right]);
    return right;
}

void quickSort(vector<int>& nums, int low, int high) {
    if (low >= high) return;

    int pivotIndex = partition(nums, low, high);
    quickSort(nums, low, pivotIndex - 1);
    quickSort(nums, pivotIndex + 1, high);
}
```

Average time: `O(n log n)`; worst time: `O(n²)`.

Choosing the first element as pivot performs badly on already sorted input. A randomized pivot greatly reduces the chance of the worst case.

`std::sort` is normally preferred in application code. It uses introsort, which combines quick sort, heap sort, and insertion sort.
