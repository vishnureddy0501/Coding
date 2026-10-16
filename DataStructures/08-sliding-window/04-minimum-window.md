# 4. Minimum-Window Problems

For a minimum window:

1. expand right until the window becomes valid;
2. shrink left while it remains valid;
3. record the smallest valid length.

## Minimum size subarray sum

This solution assumes all numbers are positive.

```cpp
int minSubArrayLen(int target, vector<int>& nums) {
    int left = 0;
    long long sum = 0;
    int answer = INT_MAX;

    for (int right = 0; right < nums.size(); ++right) {
        sum += nums[right];

        while (sum >= target) {
            answer = min(answer, right - left + 1);
            sum -= nums[left++];
        }
    }

    return answer == INT_MAX ? 0 : answer;
}
```

## Minimum Window Substring idea

Maintain:

- required frequency of every character;
- current window frequency;
- number of requirements currently satisfied.

Expand until all requirements are satisfied, then shrink while they remain satisfied. This is the most important advanced sliding-window problem.
