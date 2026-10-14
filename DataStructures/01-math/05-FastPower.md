Binary exponentiation: base^exp in O(log exp)
  exp odd  -> take one base into result, exp - 1
  exp even -> square the base, halve exp
With modulo: do result = result * base % MOD and base = base * base % MOD.
LeetCode 50 Pow(x, n): n can be negative -> compute for -n (as long long) and return 1 / result.

long long power(long long base, long long exp) {
    long long result = 1;
    while (exp > 0) {
        if (exp % 2 == 1) {
            result *= base;
			exp--;
        } else {
			base = base*base;
			exp = exp/2;
		}
    }
    return result;
}
