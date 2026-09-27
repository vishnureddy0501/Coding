# Word Ladder II

Return every shortest sequence that changes `beginWord` into `endWord`, changing one character at a time. Every intermediate word must exist in the dictionary.

## Main Idea

Use BFS because every transformation has equal cost. BFS discovers words level by level, so the first level that reaches the target gives the shortest distance.

The important rule is:

> Remove words only after finishing the complete BFS level.

Different paths on the same level may need to use the same word. Removing it immediately can lose valid shortest sequences.

## Simple Interview Approach

Store complete paths in the queue:

```text
queue: [hit]
       [hit, hot]
       [hit, hot, dot]
       ...
```

For every BFS level:

1. Generate all one-character transformations.
2. Add valid transformations to copied paths.
3. Remember every word used on this level.
4. After the level ends, remove those words from the dictionary.
5. Stop after the first level that reaches `endWord`.

This approach is easy to explain but can use a lot of memory because the queue stores entire paths.

## More Efficient Approach

For large inputs:

1. Use BFS to calculate the shortest distance to each word.
2. Record valid parent relationships on shortest paths.
3. Use DFS/backtracking from `endWord` to build all sequences.

This avoids storing every partial path in the BFS queue.

## Complexity Note

The number of shortest sequences can itself be very large, so output size affects the final time and space complexity.

## Interview Summary

- Word Ladder I asks for the shortest length: normal BFS is enough.
- Word Ladder II asks for all shortest paths: BFS establishes shortest levels, then paths are collected.
- Do not remove a word until the whole current level has finished.
