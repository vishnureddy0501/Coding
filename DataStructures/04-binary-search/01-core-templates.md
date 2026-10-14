# 1. Core templates

## Exact value in a sorted array

Use this when you only need to know whether the target exists or need any matching index.

```cpp
int binarySearch(const vector<int>& nums, int target) {
    int low = 0;
    int high = static_cast<int>(nums.size()) - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (nums[mid] == target) return mid;
        if (nums[mid] < target) low = mid + 1;
        else high = mid - 1;
    }

    return -1;
}
```

### Why `low <= high`?

Both ends are included: `[low, high]`. When `low == high`, one value is still left to check.

## First true template

Many binary-search problems can be viewed as:

```text
false false false | true true true
                  ^ first true
```

```cpp
int firstTrue(int low, int high) {
    int answer = high + 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (isPossible(mid)) {
            answer = mid;
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }

    return answer;
}
```

Use it for the minimum possible answer.

## Last true template

```text
true true true | false false false
              ^ last true
```

```cpp
int lastTrue(int low, int high) {
    int answer = low - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (isPossible(mid)) {
            answer = mid;
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    return answer;
}
```

Use it for the maximum possible answer.

## Checklist before coding

1. What is my search space?
2. Is it sorted or is the condition monotonic?
3. Am I looking for an exact value, first true, or last true?
4. What should happen when `isPossible(mid)` succeeds?
5. What answer should be returned if nothing is found?
