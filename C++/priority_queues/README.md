# C++ Priority Queues

Study these notes in order:

1. [Priority Queue Basics](./1.basics.md)
2. [Pairs and Custom Comparators](./2.pairs-and-comparators.md)
3. [Important Interview Patterns](./3.interview-patterns.md)

## Quick Revision

```cpp
// Max heap: largest value at the top
priority_queue<int> maxHeap;

// Min heap: smallest value at the top
priority_queue<int, vector<int>, greater<int>> minHeap;
```

A priority queue is useful whenever you repeatedly need the smallest or largest available element.

