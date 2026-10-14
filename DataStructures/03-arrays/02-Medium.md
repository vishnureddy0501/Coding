Pascals Triangle:
------------------
find the value at row r, column c : (r-1) C (c-1)

efficient code for calculating ncr:
-----------------------------------

long long nCr(int n, int r) {
    if (r > n - r) r = n - r; // because C(n, r) == C(n, n-r)

    long long res = 1;
    for (int i = 0; i < r; i++) {
        res *= (n - i);
        res /= (i + 1);
    }
    return res;
}

find kth row in pascals Triangle:
--------------------------------

vector<long long int> geerateRow(int k) 
{
	// number of elements in kth row = k
	vector<long long> res;
	res.push_back(1);
	long long ans = 1;
	for (long long i = 1; i < k; i++) {
		ans = ans*(k-i);
		ans = ans / i;
		res.push_back(ans);
	}
	return res;
	
} 


geerate whole pascals Triangle:
-------------------------------
vector<vector<int>> pascalsTriangle (int n) {
	vector<vector<int>> res;
	for (int i = 1; i<=n; i++) {
		res.push_back(geerateRow(i));
	}
	return res;
}

3 sum problem:
----------------
mind blowing Leetcode code

Sort, fix nums[i], then two pointers on the rest. Skip duplicates at every level.

vector<vector<int>> threeSum(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> res;
    int n = nums.size();
    for (int i = 0; i < n; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int j = i + 1, k = n - 1;
        while (j < k) {
            int sum = nums[i] + nums[j] + nums[k];
            if (sum < 0) j++;
            else if (sum > 0) k--;
            else {
                res.push_back({nums[i], nums[j], nums[k]});
                j++; k--;
                while (j < k && nums[j] == nums[j - 1]) j++;
                while (j < k && nums[k] == nums[k + 1]) k--;
            }
        }
    }
    return res;
}
4 sum: same idea with one more outer loop (use long long for the sum).

the following problems are similar:
------------------------------------
count number of subbarys with sum k and 
count number of subbarys wiht xor k

int subarraysXor(vector<int> &nums, int x)
{
    int n = nums.size(), sum = 0, res = 0;
    unordered_map<int, int> m;
    for (int i = 0; i<n; i++) {
        sum = sum ^ nums[i];
        if (sum == x) {
            res++;
        } 

        // (sum ^x) ^ x = sum
        if (m.find(sum ^ x) != m.end()) {
            res = res + m[sum^x];
        }
        m[sum]++;
    }
    return res;
}

merge interals: 
--------------
    vector<vector<int>> merge(vector<vector<int>>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        vector<vector<int>> res;
        for (int i = 0; i<n; i++) {
            if (res.size() == 0 || res.back()[1] < nums[i][0]) {
                res.push_back(nums[i]);
            } else {
                res.back()[1] = max(res.back()[1], nums[i][1]);
            }
        }
        return res;
    }

	merge sorted arrays without extra space:
	----------------------------------------
	approach 1:
	----------
	void mergeTwoSortedArraysWithoutExtraSpace(vector<long long> &a, vector<long long> &b){
	// Write your code here.
	int n = a.size(), m = b.size();
	for (int i = n - 1, j = 0; i >= 0 && j < m;) {
		if (a[i] < b[j]) {
			break;
		} else {
			swap(a[i], b[j]);
			i--;
			j++;
		}
	}
	sort(a.begin(), a.end());
	sort(b.begin(), b.end());
	
}

find repeating & missing number:
-----------------------------
method 1 : use hash map

method 2 : 

sum of first n natural numbers - sum of array elements = x - y;
sum of squares of first n natural numbers - sum of squares of array elements = pow(x, 2) - pow(y, 2);

solve above both equations


count inversions:
-----------------
Inversion: i < j and a[i] > a[j].
Use merge sort. While merging, if left[i] > right[j], then ALL remaining elements of the left half
(mid - i + 1 of them) are also > right[j], so add that count.

long long mergeCount(vector<int>& a, int low, int mid, int high) {
    vector<int> temp;
    long long cnt = 0;
    int i = low, j = mid + 1;
    while (i <= mid && j <= high) {
        if (a[i] <= a[j]) temp.push_back(a[i++]);
        else { cnt += mid - i + 1; temp.push_back(a[j++]); }
    }
    while (i <= mid) temp.push_back(a[i++]);
    while (j <= high) temp.push_back(a[j++]);
    for (int k = low; k <= high; k++) a[k] = temp[k - low];
    return cnt;
}

long long countInversions(vector<int>& a, int low, int high) {
    if (low >= high) return 0;
    int mid = low + (high - low) / 2;
    return countInversions(a, low, mid) + countInversions(a, mid + 1, high) + mergeCount(a, low, mid, high);
}

Reverse pairs (a[i] > 2 * a[j]): same, but count with a separate two-pointer pass BEFORE merging.
