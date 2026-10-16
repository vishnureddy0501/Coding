# 1. Core Idea

Backtracking tries one choice, explores it, and then removes that choice.

```text
Choose -> Explore -> Undo -> Try next choice
```

## Basic template

```cpp
void solve(/* current state */) {
    if (/* answer is complete */) {
        // store or return the answer
        return;
    }

    for (/* every possible choice */) {
        if (/* choice is invalid */) continue;

        // choose

        solve(/* next state */);

        // undo the choice
    }
}
```

## Simple example

Create all strings of length `n` using `A` and `B`:

```cpp
void generate(int n, string& current, vector<string>& answer) {
    if (current.size() == n) {
        answer.push_back(current);
        return;
    }

    current.push_back('A');
    generate(n, current, answer);
    current.pop_back();

    current.push_back('B');
    generate(n, current, answer);
    current.pop_back();
}
```

`pop_back()` is the undo step. Without it, the next choice starts with the wrong state.

## How to design a solution

Answer four questions:

1. What is one choice?
2. When is a choice invalid?
3. When is the answer complete?
4. What must be undone before trying the next choice?

## Complexity

Backtracking is usually exponential because it explores many choices.

Examples:

- Subsets: `O(2^n)` answers.
- Permutations: `O(n!)` answers.

If the question asks you to return every answer, this cost is often unavoidable.

