# Gray Code

Convert a non-negative integer to Gray code with:

```cpp
int gray = num ^ (num >> 1);
```

For a binary string, first parse it as a binary number and then apply the same formula.
