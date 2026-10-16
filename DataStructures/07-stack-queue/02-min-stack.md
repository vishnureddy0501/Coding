# 2. Min Stack

Store the current minimum together with every value. This is the simplest interview solution.

```cpp
class MinStack {
    stack<pair<int, int>> values;

public:
    void push(int value) {
        int minimum = values.empty()
            ? value
            : min(value, values.top().second);

        values.push({value, minimum});
    }

    void pop() {
        values.pop();
    }

    int top() {
        return values.top().first;
    }

    int getMin() {
        return values.top().second;
    }
};
```

All operations: `O(1)`; extra space: `O(n)`.

An encoding trick can achieve `O(1)` extra space using `2 * value - minimum`, but it is harder to explain and can overflow without `long long`. Use it only when constant extra space is specifically requested.
