# 4. Monotonic Stack

A monotonic stack keeps values or indices in increasing or decreasing order. Every item is pushed and popped at most once, so the total time is `O(n)`.

## Next greater element

Traverse from right to left and remove values that cannot be the answer.

```cpp
vector<int> nextGreaterElements(vector<int>& nums) {
    int n = nums.size();
    vector<int> answer(n, -1);
    stack<int> values;

    for (int i = n - 1; i >= 0; --i) {
        while (!values.empty() && values.top() <= nums[i]) {
            values.pop();
        }

        if (!values.empty()) answer[i] = values.top();
        values.push(nums[i]);
    }

    return answer;
}
```

For a circular array, iterate from `2 * n - 1` down to `0` and access `nums[i % n]`.

## Largest rectangle in a histogram

Store indices of increasing bar heights. When a shorter bar arrives, calculate rectangles ending before it.

```cpp
int largestRectangleArea(vector<int>& heights) {
    stack<int> indices;
    int answer = 0;

    for (int i = 0; i <= heights.size(); ++i) {
        int currentHeight = i == heights.size() ? 0 : heights[i];

        while (!indices.empty() && heights[indices.top()] > currentHeight) {
            int height = heights[indices.top()];
            indices.pop();

            int leftBoundary = indices.empty() ? -1 : indices.top();
            int width = i - leftBoundary - 1;
            answer = max(answer, height * width);
        }

        indices.push(i);
    }

    return answer;
}
```

## Duplicate-handling rule

For problems such as Sum of Subarray Minimums, one side should use a strict comparison and the other a non-strict comparison. This prevents equal values from counting the same subarray twice.

```text
One side:  pop while >=
Other side: pop while >
```
