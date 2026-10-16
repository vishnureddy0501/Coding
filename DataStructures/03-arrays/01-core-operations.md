# 1. Core Operations

## Remove duplicates from a sorted array

```cpp
int removeDuplicates(vector<int>& nums) {
    if (nums.empty()) return 0;

    int write = 1;

    for (int read = 1; read < nums.size(); ++read) {
        if (nums[read] != nums[write - 1]) {
            nums[write] = nums[read];
            ++write;
        }
    }

    return write;
}
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

    while (i < first.size() || j < second.size()) {
        int value;

        if (j == second.size() ||
            (i < first.size() && first[i] <= second[j])) {
            value = first[i++];
        } else {
            value = second[j++];
        }

        if (result.empty() || result.back() != value) {
            result.push_back(value);
        }
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
