# Binary Search

Binary search repeatedly removes half of the search space.

## When should you think about it?

Use binary search when at least one of these is true:

1. The array is sorted, rotated-sorted, or has a predictable order.
2. A condition changes only once:

```text
false false false true true true
```

3. The question asks for the minimum or maximum possible answer, and you can check whether a candidate answer is possible.

Do not assume every maximize/minimize problem needs binary search. The feasibility condition must be monotonic.

## Complexity

```text
Search space size: n
Time: O(log n)
Extra space: O(1)
```

For binary search on an answer, total time is usually:

```text
O(check-function cost × log(answer range))
```

## Study order

1. [Core templates](01-core-templates.md)
2. [Bounds and occurrences](02-bounds-and-occurrences.md)
3. [Rotated arrays and peaks](03-rotated-and-peak.md)
4. [Binary search on the answer](04-binary-search-on-answer.md)
5. [Important problems](05-important-problems.md)

## One rule that prevents many bugs

```cpp
int mid = low + (high - low) / 2;
```

Prefer this over `(low + high) / 2` because `low + high` can overflow.
