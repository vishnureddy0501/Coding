void segmentTreeBuild(int index, int low, int high) {
	if (low == high) {                  // leaf: store the array value
		segmentTree[index] = nums[low];
		return;
	}
	int mid = (low + high)/2;
	int leftIndex = (2*index) + 1, rightIndex = (2*index) + 2; // these are standard formulas. need to remember
	segmentTreeBuild(leftIndex, low, mid);
	segmentTreeBuild(rightIndex, mid + 1, high);   // mid + 1, not mid (infinite recursion)
	segmentTree[index] = min(segmentTree[leftIndex], segmentTree[rightIndex]);
}
vector<int> nums = {1, 2, 4, 10};
vector<int> segmentTree(4*nums.size()); // this is also standard formula. we need to remember
segmentTreeBuild(0, 0, n-1);