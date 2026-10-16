# 1. Basics and Implementations

## Stack

Last in, first out.

```cpp
stack<int> values;
values.push(10);
values.top();
values.pop();
values.empty();
```

## Queue

First in, first out.

```cpp
queue<int> values;
values.push(10);
values.front();
values.pop();
values.empty();
```

## Implement stack using one queue

After inserting a value, rotate the older values behind it. The queue front then acts as the stack top.

```cpp
class MyStack {
    queue<int> values;

public:
    void push(int value) {
        values.push(value);
        int olderValues = values.size() - 1;

        while (olderValues-- > 0) {
            values.push(values.front());
            values.pop();
        }
    }

    int pop() {
        int value = values.front();
        values.pop();
        return value;
    }

    int top() {
        return values.front();
    }

    bool empty() {
        return values.empty();
    }
};
```

Push: `O(n)`; pop/top: `O(1)`.

## Implement queue using two stacks

Push into `input`. Move values to `output` only when `output` is empty.

```cpp
class MyQueue {
    stack<int> input;
    stack<int> output;

    void prepareOutput() {
        if (!output.empty()) return;

        while (!input.empty()) {
            output.push(input.top());
            input.pop();
        }
    }

public:
    void push(int value) {
        input.push(value);
    }

    int pop() {
        prepareOutput();
        int value = output.top();
        output.pop();
        return value;
    }

    int peek() {
        prepareOutput();
        return output.top();
    }

    bool empty() {
        return input.empty() && output.empty();
    }
};
```

Each value moves between stacks at most once, so pop and peek are amortized `O(1)`.
