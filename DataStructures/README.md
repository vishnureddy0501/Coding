# DSA Study Roadmap

Work through the folders in number order. Inside each folder, go file by file in number order.

| # | Folder | What's inside |
|---|--------|---------------|
| 01 | [math](01-math/) | XOR, divisors, primes, GCD/LCM, sieve, prime factors, fast power |
| 02 | [sorting](02-sorting/) | Complexity table, selection/bubble/insertion/merge/quick/counting sort |
| 03 | [arrays](03-arrays/) | Two pointers, prefix sum + hashmap, Kadane, majority element, next permutation, 3 sum, merge intervals, count inversions |
| 04 | [binary-search](04-binary-search/) | Lower/upper bound, rotated arrays, peak element, binary search on answer |
| 05 | [linked-list](05-linked-list/) | Basics, memory, slow/fast pointer, cycles, dummy nodes, merge sort, clone with random pointers |
| 06 | [bit-manipulation](06-bit-manipulation/) | Set/clear/toggle bits, `n & (n-1)`, XOR tricks, Gray code |
| 07 | [stack-queue](07-stack-queue/) | Stack ↔ queue implementations, min stack, expression conversion, monotonic stack |
| 08 | [sliding-window](08-sliding-window/) | Window template, counting subarrays, practice list |
| 09 | [trees](09-trees/) | Tree types, traversals, level order, views, vertical order, must-do problems, BST |
| 10 | [graphs](10-graphs/) | Has its own [README](10-graphs/README.md): BFS/DFS → cycles → topo sort → shortest paths → DSU/MST |
| 11 | [dynamic-programming](11-dynamic-programming/) | How to approach DP, patterns list, space optimization, coin change, print LCS |
| 99 | [revision](99-revision/) | Mixed problems to revisit |
| — | [advanced-later](advanced-later/) | **Skip for now.** Morris traversal, trie, segment tree, SCC, bridges |

## Quick pattern guide
| Problem says… | Try… |
|---|---|
| sorted array, find / min / max | Binary search |
| "minimum X such that…" / "maximum X such that…" | Binary search on answer |
| subarray / substring, longest or count | Sliding window (non-negative) or prefix sum + hashmap |
| pair / triplet with target sum | Sort + two pointers |
| next greater / smaller element | Monotonic stack |
| middle of list, cycle | Slow/fast pointer |
| level, minimum steps | BFS |
| count ways / min cost with choices | DP |
| appears once while others appear twice | XOR |
