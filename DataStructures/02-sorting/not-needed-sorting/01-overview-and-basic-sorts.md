# 1. Overview and Basic Sorts

| Algorithm | Best | Average | Worst | Extra space | Stable? |
|---|---:|---:|---:|---:|---|
| Selection sort | `O(n²)` | `O(n²)` | `O(n²)` | `O(1)` | No |
| Bubble sort | `O(n)` | `O(n²)` | `O(n²)` | `O(1)` | Yes |
| Insertion sort | `O(n)` | `O(n²)` | `O(n²)` | `O(1)` | Yes |
| Merge sort | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(n)` | Yes |
| Quick sort | `O(n log n)` | `O(n log n)` | `O(n²)` | `O(log n)` average stack | No |
| Counting sort | `O(n + k)` | `O(n + k)` | `O(n + k)` | `O(k)` | Can be stable |

Stable means equal values keep their original relative order.

## Selection sort

Find the minimum value in the unsorted portion and place it at the beginning.

```cpp
void selectionSort(vector<int>& nums) {
    int n = nums.size();

    for (int i = 0; i < n - 1; ++i) {
        int minimumIndex = i;

        for (int j = i + 1; j < n; ++j) {
            if (nums[j] < nums[minimumIndex]) minimumIndex = j;
        }

        swap(nums[i], nums[minimumIndex]);
    }
}
```

## Bubble sort

Repeatedly swap adjacent out-of-order values. Larger values move to the right.

```cpp
void bubbleSort(vector<int>& nums) {
    int n = nums.size();

    for (int end = n - 1; end > 0; --end) {
        bool swapped = false;

        for (int i = 0; i < end; ++i) {
            if (nums[i] > nums[i + 1]) {
                swap(nums[i], nums[i + 1]);
                swapped = true;
            }
        }

        if (!swapped) break;
    }
}
```

The number of bubble-sort swaps equals the number of inversions.

## Insertion sort

Keep the left portion sorted and insert the current value into it.

```cpp
void insertionSort(vector<int>& nums) {
    for (int i = 1; i < nums.size(); ++i) {
        int value = nums[i];
        int j = i - 1;

        while (j >= 0 && nums[j] > value) {
            nums[j + 1] = nums[j];
            --j;
        }

        nums[j + 1] = value;
    }
}
```

Insertion sort is useful for small or nearly sorted inputs.
