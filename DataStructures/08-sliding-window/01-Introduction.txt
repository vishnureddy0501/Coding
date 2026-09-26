standard pattern for sliding window:
----------------------------------
No need to write clumsy if-else conditions.

for loop {
	// consditions

	while loop / for loop

	// conditions.
}


Sliding window approaches:
---------------------------

1. longest subarray with sum <= k

2. Number of subarrays where <condition>
	it is tough to figure out weather to shrink or expand.

	example: number of subarrays where sum = k 
	-------
	Hence (number of subarray where sum <= k) - (number of subarrays where sum <= k-1)
	(works only when all numbers are non-negative. With negatives use prefix sum + hashmap.)


Clean template (longest window satisfying a condition):
-------------------------------------------------------
    int l = 0, res = 0;
    for (int r = 0; r < n; r++) {
        add(nums[r]);
        while (windowInvalid()) {
            remove(nums[l]);
            l++;
        }
        res = max(res, r - l + 1);
    }

Count subarrays with condition <= k: inside the same loop do count += r - l + 1
(every subarray ending at r and starting in [l, r] is valid).