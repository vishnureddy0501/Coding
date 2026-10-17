# Important Tricky Array Problems

This list focuses on medium and high-value hard problems that commonly cause mistakes in interviews.

Company names are commonly reported public tags, not official guarantees.

## 1. Prefix sum and hashing

| Priority | Problem | What makes it tricky | Commonly reported companies |
|---|---|---|---|
| ⭐⭐⭐⭐⭐ | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Store prefix frequency, not only existence | Meta, Amazon, Google |
| ⭐⭐⭐⭐⭐ | [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/) | Same remainder and length at least two | Meta, Amazon, Microsoft |
| ⭐⭐⭐⭐⭐ | Count Subarrays with XOR K | Prefix XOR + frequency map | Amazon, Microsoft, Adobe |
| ⭐⭐⭐⭐⭐ | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Start only at the beginning of a sequence | Google, Amazon, Microsoft |
| ⭐⭐⭐⭐ | [Contiguous Array](https://leetcode.com/problems/contiguous-array/) | Convert `0` to `-1` and store first index | Meta, Amazon, Google |
| ⭐⭐⭐⭐ | [4Sum II](https://leetcode.com/problems/4sum-ii/) | Split into two pair sums | Amazon, Microsoft, Apple |

## 2. Two pointers and ordering

| Priority | Problem | What makes it tricky | Commonly reported companies |
|---|---|---|---|
| ⭐⭐⭐⭐⭐ | [3Sum](https://leetcode.com/problems/3sum/) | Sorting and duplicate skipping | Meta, Amazon, Microsoft |
| ⭐⭐⭐⭐⭐ | [4Sum](https://leetcode.com/problems/4sum/) | Duplicate skipping and `long long` overflow | Amazon, Microsoft, Google |
| ⭐⭐⭐⭐⭐ | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Move only the shorter side | Amazon, Meta, Google |
| ⭐⭐⭐⭐⭐ | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Correct left/right maximum reasoning | Amazon, Meta, Google |
| ⭐⭐⭐⭐ | [Boats to Save People](https://leetcode.com/problems/boats-to-save-people/) | Pair the heaviest greedily | Amazon, Microsoft, Google |

## 3. Array transformations

| Priority | Problem | What makes it tricky | Commonly reported companies |
|---|---|---|---|
| ⭐⭐⭐⭐⭐ | [Next Permutation](https://leetcode.com/problems/next-permutation/) | Find pivot, swap, then reverse suffix | Meta, Google, Amazon |
| ⭐⭐⭐⭐⭐ | [Product Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Prefix and suffix without division | Meta, Amazon, Microsoft |
| ⭐⭐⭐⭐⭐ | [Sort Colors](https://leetcode.com/problems/sort-colors/) | Three pointers and rechecking swapped values | Amazon, Microsoft, Meta |
| ⭐⭐⭐⭐ | [Rotate Array](https://leetcode.com/problems/rotate-array/) | Three reversals and `k % n` | Amazon, Microsoft, Google |
| ⭐⭐⭐⭐ | [Rearrange Array Elements by Sign](https://leetcode.com/problems/rearrange-array-elements-by-sign/) | Correct positive/negative positions | Amazon, Microsoft |

## 4. Kadane and greedy arrays

| Priority | Problem | What makes it tricky | Commonly reported companies |
|---|---|---|---|
| ⭐⭐⭐⭐⭐ | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | All-negative arrays | Amazon, Microsoft, Bloomberg |
| ⭐⭐⭐⭐⭐ | [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | Track both minimum and maximum | Amazon, Google, Microsoft |
| ⭐⭐⭐⭐⭐ | [Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Greedy level boundary | Amazon, Google, Microsoft |
| ⭐⭐⭐⭐⭐ | [Gas Station](https://leetcode.com/problems/gas-station/) | Total feasibility versus current failure | Amazon, Google, Microsoft |
| ⭐⭐⭐⭐ | [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | Take every positive increase | Amazon, Microsoft, Meta |
| ⭐⭐⭐⭐ | [Candy](https://leetcode.com/problems/candy/) | Satisfy constraints from both directions | Google, Amazon, Microsoft |

## 5. Intervals

| Priority | Problem | What makes it tricky | Commonly reported companies |
|---|---|---|---|
| ⭐⭐⭐⭐⭐ | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Sort and compare with the last merged interval | Meta, Google, Amazon |
| ⭐⭐⭐⭐⭐ | [Insert Interval](https://leetcode.com/problems/insert-interval/) | Before, overlapping, and after sections | Meta, Amazon, Google |
| ⭐⭐⭐⭐ | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Keep the interval ending earliest | Google, Amazon, Microsoft |
| ⭐⭐⭐⭐ | [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | Move the interval that finishes first | Meta, Amazon, Google |

## 6. Matrix problems

| Priority | Problem | What makes it tricky | Commonly reported companies |
|---|---|---|---|
| ⭐⭐⭐⭐⭐ | [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | First row and column as markers | Amazon, Microsoft, Meta |
| ⭐⭐⭐⭐⭐ | [Rotate Image](https://leetcode.com/problems/rotate-image/) | Transpose and reverse | Amazon, Microsoft, Apple |
| ⭐⭐⭐⭐ | [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Avoid repeating rows or columns | Amazon, Microsoft, Google |
| ⭐⭐⭐⭐ | [Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/) | Start at top-right or bottom-left | Amazon, Microsoft, Google |

## 7. Index-placement and cycle tricks

| Priority | Problem | What makes it tricky | Commonly reported companies |
|---|---|---|---|
| ⭐⭐⭐⭐⭐ | [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) | Treat values as linked-list pointers | Amazon, Microsoft, Google |
| ⭐⭐⭐⭐⭐ | [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) | Place value `x` at index `x - 1` | Amazon, Google, Meta |
| ⭐⭐⭐⭐ | Missing and Repeating Number | Math/XOR/index placement | Amazon, Microsoft, Adobe |

## Best revision set

Do not miss these twelve:

1. Subarray Sum Equals K
2. Longest Consecutive Sequence
3. 3Sum
4. Next Permutation
5. Product Except Self
6. Maximum Product Subarray
7. Merge Intervals
8. Insert Interval
9. Set Matrix Zeroes
10. Rotate Image
11. Find the Duplicate Number
12. First Missing Positive

## Common interview traps

- Integer overflow in 4Sum and large prefix sums.
- Incorrect duplicate skipping in 3Sum and 4Sum.
- Assuming Kadane works only when a positive number exists.
- Forgetting that prefix maps often store frequencies or first indices.
- Incorrect interval boundary handling.
- Modifying the first matrix row/column before saving their original state.
- Using extra space when the interviewer asks for an in-place solution.
