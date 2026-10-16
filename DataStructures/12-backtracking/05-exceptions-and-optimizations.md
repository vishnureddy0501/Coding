# 5. Important Exceptions and Optimizations

## Always undo changed state

If you add, mark, or modify something before recursion, restore it afterward.

```cpp
current.push_back(value); // choose
solve();                  // explore
current.pop_back();       // undo
```

## Store a copy of the answer

```cpp
answer.push_back(current);
```

Do not store a reference to a temporary state that will change later.

## Stop invalid branches early

This is called pruning.

Examples:

- Remaining sum becomes negative.
- Current string already violates a rule.
- Not enough values remain to complete the answer.
- A queen attacks the current position.

## Duplicate inputs

Usually:

1. Sort the input.
2. Skip equal choices at the same recursion level.

Do not put every generated answer into a set unless necessary. It wastes time and memory.

## One answer versus all answers

- Need one answer: return `bool` and stop when found.
- Need all answers: use a result vector and continue.
- Need only the count: return a number instead of storing every answer.

## Backtracking versus DP

```text
Generate every valid result       -> backtracking
Same state is solved repeatedly   -> memoization / DP may help
```

Memoization is useful only when the result depends completely on a reusable state. It usually does not help when every path must be returned.

## Common mistakes

- Forgetting the undo step.
- Using the wrong next index.
- Incorrect base case.
- Adding the answer too early or too late.
- Failing to sort before duplicate skipping.
- Sharing visited state between separate starting paths.
- Modifying a grid cell and not restoring it.
- Forgetting that output size may already be exponential.

