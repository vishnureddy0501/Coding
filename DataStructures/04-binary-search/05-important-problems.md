# 5. Important problems

Solve them in this order. Do not try to finish every problem in one sitting.

## Level 1 — foundations

| # | Problem | Main idea |
|---:|---|---|
| 1 | LeetCode 704 — Binary Search | Exact search template |
| 2 | LeetCode 35 — Search Insert Position | Lower bound |
| 3 | LeetCode 34 — First and Last Position | Lower + upper bound |
| 4 | Count Occurrences in Sorted Array | `upper_bound - lower_bound` |
| 5 | Floor and Ceil in Sorted Array | Bound variations |
| 6 | LeetCode 69 — Sqrt(x) | Search numeric answer |

## Level 2 — important array patterns

| # | Problem | Main idea |
|---:|---|---|
| 7 | LeetCode 33 — Search in Rotated Sorted Array | Identify sorted half |
| 8 | LeetCode 81 — Search in Rotated Sorted Array II | Handle duplicates |
| 9 | LeetCode 153 — Find Minimum in Rotated Sorted Array | Compare with right end |
| 10 | LeetCode 162 — Find Peak Element | Move toward rising side |
| 11 | LeetCode 540 — Single Element in Sorted Array | Pair-index pattern |
| 12 | LeetCode 1539 — Kth Missing Positive Number | Missing count formula |

## Level 3 — binary search on answer

| # | Problem | Minimize or maximize? |
|---:|---|---|
| 13 | LeetCode 875 — Koko Eating Bananas | Minimum speed |
| 14 | LeetCode 1482 — Minimum Days to Make Bouquets | Minimum day |
| 15 | LeetCode 1011 — Capacity to Ship Packages | Minimum capacity |
| 16 | Aggressive Cows | Maximum minimum distance |
| 17 | LeetCode 1552 — Magnetic Force Between Two Balls | Maximum minimum distance |
| 18 | Book Allocation | Minimum maximum pages |
| 19 | LeetCode 410 — Split Array Largest Sum | Minimum largest sum |
| 20 | Painter's Partition | Minimum completion time |

## Level 4 — interview hard problems

| # | Problem | Main idea |
|---:|---|---|
| 21 | LeetCode 4 — Median of Two Sorted Arrays | Partition two arrays |
| 22 | Kth Element of Two Sorted Arrays | Partition two arrays |
| 23 | LeetCode 378 — Kth Smallest in Sorted Matrix | Count values `<= mid` |
| 24 | LeetCode 774 — Minimize Max Distance to Gas Station | Binary search on decimal answer |

## Minimum revision set

If you have little time, repeatedly solve these eight:

1. Binary Search
2. First and Last Position
3. Search in Rotated Sorted Array
4. Find Minimum in Rotated Sorted Array
5. Find Peak Element
6. Koko Eating Bananas
7. Capacity to Ship Packages
8. Aggressive Cows

## Practice method

For each problem, first write these four lines on paper:

```text
Search space:
Monotonic condition:
When condition succeeds:
Return value:
```

If stuck, identify the search space and condition before looking at code. After solving, repeat the problem after 2 days and again after 1 week.
