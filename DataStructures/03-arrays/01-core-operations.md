# 1. Core Operations

## Remove duplicates from a sorted array

```cpp
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int n = nums.size();
        int start = 1;

        for (int i = 1; i < n; i++) {
            if (nums[i] == nums[i - 1]) {
                // Duplicate: do not increment start.
            } else {
                nums[start++] = nums[i];
            }
        }

        return start;
    }
};
```

## Move zeroes to the end

```cpp
void moveZeroes(vector<int>& nums) {
    int write = 0;

    for (int value : nums) {
        if (value != 0) nums[write++] = value;
    }

    while (write < nums.size()) {
        nums[write++] = 0;
    }
}
```

## Union of two sorted arrays

```cpp
vector<int> sortedUnion(vector<int>& first, vector<int>& second) {
    vector<int> result;
    int i = 0;
    int j = 0;

    while (i < first.size() && j < second.size()) {
        if (first[i] <= second[j]) {
            if (result.empty() || result.back() != first[i]) {
                result.push_back(first[i]);
            }
            i++;
        } else {
            if (result.empty() || result.back() != second[j]) {
                result.push_back(second[j]);
            }
            j++;
        }
    }

    while (i < first.size()) {
        if (result.empty() || result.back() != first[i]) {
            result.push_back(first[i]);
        }
        i++;
    }

    while (j < second.size()) {
        if (result.empty() || result.back() != second[j]) {
            result.push_back(second[j]);
        }
        j++;
    }

    return result;
}
```

## Check whether an array is monotonic

```cpp
bool isMonotonic(vector<int>& nums) {
    bool increasing = true;
    bool decreasing = true;

    for (int i = 1; i < nums.size(); ++i) {
        if (nums[i] < nums[i - 1]) increasing = false;
        if (nums[i] > nums[i - 1]) decreasing = false;
    }

    return increasing || decreasing;
}
```
