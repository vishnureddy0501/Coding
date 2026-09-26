1. check if kth bit is set or not. 
	(num >> k) & 1 

	if above value is 1 then bit is set. 
	else bit is not set.


2. How to turn on a bit. 
	(1 << i) | num

	if i = 2:
	   then (1 << i) becomes 100

	   100 | num gives the result by changing ith bit from right to 1 


3. 1 << i  [Very Optimal when compared to pow]
	it is same as pow(2, i);

	the above expression left shifts binary represention i times.


4. Clear the ith bit:   num & ~(1 << i)
5. Toggle the ith bit:  num ^ (1 << i)
6. Remove the last set bit:  num & (num - 1)
	power of 2 check: num > 0 && (num & (num - 1)) == 0
7. Get the last set bit:  num & (-num)
8. Count set bits:
	while (num) { num = num & (num - 1); count++; }     // runs once per set bit
	or __builtin_popcount(num)   (__builtin_popcountll for long long)
9. Swap without temp: a = a ^ b; b = a ^ b; a = a ^ b;
10. XOR tricks: a ^ a = 0, a ^ 0 = a
	single number (every other appears twice): XOR everything
	XOR of 1..n: n % 4 == 0 -> n, 1 -> 1, 2 -> n + 1, 3 -> 0
11. Subsets using bits: for mask in 0 .. (1 << n) - 1, element i is taken if (mask >> i) & 1

Careful: 1 << 31 overflows int. Use 1LL << i for i >= 31.
