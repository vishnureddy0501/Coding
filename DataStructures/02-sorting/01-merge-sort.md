# 1. Merge Sort

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

## Reverse Pairs

A reverse pair satisfies:

```text
i < j and nums[i] > 2 * nums[j]
```

Count the pairs after sorting both halves but before merging them.

```cpp
class Solution {
public:
    void merge(vector<int>& nums, int low, int mid, int high) {
        vector<int> res;
        int left = low, right = mid + 1;

        while (left <= mid && right <= high) {
            if (nums[left] <= nums[right]) {
                res.push_back(nums[left]);
                left++;
            } else {
                res.push_back(nums[right]);
                right++;
            }
        }

        while (left <= mid) {
            res.push_back(nums[left]);
            left++;
        }

        while (right <= high) {
            res.push_back(nums[right]);
            right++;
        }

        for (int i = low; i <= high; i++) {
            nums[i] = res[i - low];
        }
    }

    int countPairs(vector<int>& nums, int low, int mid, int high) {
        int count = 0;
        int right = mid + 1;

        for (int left = low; left <= mid; left++) {
            while (right <= high &&
                   (long long)nums[left] > 2LL * nums[right]) {
                right++;
            }

            count += right - (mid + 1);
        }

        return count;
    }

    void mergeSortAlgo(vector<int>& nums, int low, int high, int& ans) {
        if (low >= high) return;

        int mid = low + (high - low) / 2;

        mergeSortAlgo(nums, low, mid, ans);
        mergeSortAlgo(nums, mid + 1, high, ans);

        ans += countPairs(nums, low, mid, high);
        merge(nums, low, mid, high);
    }

    int reversePairs(vector<int>& nums) {
        int ans = 0;
        mergeSortAlgo(nums, 0, nums.size() - 1, ans);
        return ans;
    }
};
```

Why count before merging? Both halves must remain separately sorted while counting cross-half pairs.

Use `2LL * nums[right]` to prevent integer overflow.

Time: `O(n log n)`; extra space: `O(n)`.
