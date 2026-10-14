# 3. Rotated arrays and peaks

## Search in a rotated sorted array

A rotated array is not fully sorted, but at least one half around `mid` is sorted.

```cpp
int searchRotated(vector<int>& nums, int target) {
    int low = 0;
    int high = nums.size() - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (nums[mid] == target) return mid;

        if (nums[low] <= nums[mid]) { // Left half is sorted.
            if (nums[low] <= target && target < nums[mid]) {
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        } else { // Right half is sorted.
            if (nums[mid] < target && target <= nums[high]) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
    }

    return -1;
}
```

Notice the strict comparison around `mid`; equality was already checked.

## Rotated array with duplicates

Duplicates can hide which half is sorted.

```cpp
bool searchRotatedWithDuplicates(vector<int>& nums, int target) {
    int low = 0;
    int high = nums.size() - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (nums[mid] == target) return true;

        if (nums[low] == nums[mid] && nums[mid] == nums[high]) {
            ++low;
            --high;
        } else if (nums[low] <= nums[mid]) {
            if (nums[low] <= target && target < nums[mid]) high = mid - 1;
            else low = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[high]) low = mid + 1;
            else high = mid - 1;
        }
    }

    return false;
}
```

Worst-case time becomes `O(n)` when many values are identical.

## Minimum in a rotated sorted array

```cpp
class Solution {
public:
    int findMin(vector<int>& nums) {
        int n = nums.size();
        int result = INT_MAX;

        for (int low = 0, high = n - 1; low <= high;) {
            int mid = low + (high - low) / 2;
            result = min(result, nums[mid]);

            if (nums[mid] < nums[high]) {
                // The right portion is sorted. nums[mid] is its minimum,
                // and it is already included in result, so search left.
                high = mid - 1;
            } else {
                // Rotation point and minimum must be to the right of mid.
                low = mid + 1;
            }
        }

        return result;
    }
};
```

The important step is updating `result` before removing either half. Therefore, when the right portion is sorted, it is safe to use `high = mid - 1`: `nums[mid]`, the smallest value in that sorted portion, has already been saved.

This version assumes the array contains distinct values, as in LeetCode 153.

## Peak element

A peak is greater than both of its neighbours.

Handle the boundary elements first. The binary-search loop can then safely use `mid - 1` and `mid + 1` without going outside the array.

```cpp
int findPeakElement(vector<int>& nums) {
    int n = nums.size();

    if (n == 1) return 0;
    if (nums[0] > nums[1]) return 0;
    if (nums[n - 1] > nums[n - 2]) return n - 1;

    int low = 1;
    int high = n - 2;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (nums[mid - 1] < nums[mid] && nums[mid] > nums[mid + 1]) {
            return mid;
        }

        if (nums[mid - 1] < nums[mid] && nums[mid] < nums[mid + 1]) {
            // The values are increasing, so a peak exists on the right.
            low = mid + 1;
        } else {
            // The values are decreasing, or mid is in a valley.
            // A peak exists on the left.
            high = mid - 1;
        }
    }

    return -1;
}
```

### Direction idea

```text
nums[mid - 1] < nums[mid] < nums[mid + 1]
                         rising ↗  search right

nums[mid - 1] > nums[mid] > nums[mid + 1]
             falling ↘             search left

nums[mid - 1] > nums[mid] < nums[mid + 1]
             valley                either side has a peak;
                                   this code searches left
```

The problem guarantees that adjacent values are different. It also treats values outside the array as negative infinity, so at least one peak always exists.

Time: `O(log n)`; extra space: `O(1)`.
