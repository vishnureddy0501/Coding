# 2. Counting Sort — Crux Only

Count how many times each value occurs, then rebuild the sorted array.

```text
[3, 1, 1, 2]

frequency: 1 -> 2 times, 2 -> 1 time, 3 -> 1 time
result:    [1, 1, 2, 3]
```

Use it only when values are non-negative integers in a small range.
