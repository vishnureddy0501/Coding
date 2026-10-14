# 2. Bounds and occurrences

Consider:

```text
nums = [1, 3, 3, 5, 7, 8, 8, 10]
```

## Lower bound

The first index whose value is `>= target`.

```cpp
int lowerBound(const vector<int>& nums, int target) {
    int low = 0;
    int high = static_cast<int>(nums.size()) - 1;
    int answer = nums.size();

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (nums[mid] >= target) {
            answer = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }

    return answer;
}
```

Examples:

```text
lowerBound(5)  = 3  // nums[3] = 5
lowerBound(6)  = 4  // nums[4] = 7
lowerBound(11) = 8  // nums.size(), no valid element
```

## Upper bound

The first index whose value is `> target`.

```cpp
int upperBound(const vector<int>& nums, int target) {
    int low = 0;
    int high = static_cast<int>(nums.size()) - 1;
    int answer = nums.size();

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (nums[mid] > target) {
            answer = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }

    return answer;
}
```

## C++ built-ins

```cpp
int lower = lower_bound(nums.begin(), nums.end(), target) - nums.begin();
int upper = upper_bound(nums.begin(), nums.end(), target) - nums.begin();
```

## First and last occurrence

```cpp
vector<int> searchRange(vector<int>& nums, int target) {
    int first = lower_bound(nums.begin(), nums.end(), target) - nums.begin();

    if (first == nums.size() || nums[first] != target) {
        return {-1, -1};
    }

    int last = upper_bound(nums.begin(), nums.end(), target) - nums.begin() - 1;
    return {first, last};
}
```

Number of occurrences:

```cpp
int count = upper_bound(nums.begin(), nums.end(), target)
          - lower_bound(nums.begin(), nums.end(), target);
```

## Floor and ceil

```text
floor = largest value <= target
ceil  = smallest value >= target
```

The ceil index is the lower bound. The floor index is `upperBound(target) - 1`.

Always check that the resulting index is inside the array.
