# Check Whether a Number Is Prime

Check divisors only up to `sqrt(num)`. If `num` has a larger divisor, it must also have a smaller paired divisor.

```cpp
bool isPrime(int num) {
    if (num <= 1) return false;

    for (int divisor = 2; divisor <= num / divisor; ++divisor) {
        if (num % divisor == 0) return false;
    }

    return true;
}
```

Time: `O(sqrt(n))`; space: `O(1)`.
