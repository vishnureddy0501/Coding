Sorting algorithms
------------------
| Algorithm | Best      | Average   | Worst     | Space    | Stable |
|-----------|-----------|-----------|-----------|----------|--------|
| Selection | n^2       | n^2       | n^2       | 1        | No     |
| Bubble    | n         | n^2       | n^2       | 1        | Yes    |
| Insertion | n         | n^2       | n^2       | 1        | Yes    |
| Merge     | n log n   | n log n   | n log n   | n        | Yes    |
| Quick     | n log n   | n log n   | n^2       | log n    | No     |
| Counting  | n + k     | n + k     | n + k     | k        | Yes    |

Stable = equal elements keep their original order.
Interview must-know: Merge sort and Quick sort code. std::sort is introsort (quick + heap + insertion).


Selection sort: pick the minimum of the unsorted part, swap it to the front.
----------------------------------------------------------------------------
for (int i = 0; i < n - 1; i++) {
    int mini = i;
    for (int j = i + 1; j < n; j++)
        if (nums[j] < nums[mini]) mini = j;
    swap(nums[i], nums[mini]);
}


Merge sort: split into halves, sort each, merge two sorted halves.
-------------------------------------------------------------------
void merge(vector<int>& nums, int low, int mid, int high) {
    vector<int> temp;
    int i = low, j = mid + 1;
    while (i <= mid && j <= high) {
        if (nums[i] <= nums[j]) temp.push_back(nums[i++]);
        else temp.push_back(nums[j++]);
    }
    while (i <= mid) temp.push_back(nums[i++]);
    while (j <= high) temp.push_back(nums[j++]);
    for (int k = low; k <= high; k++) nums[k] = temp[k - low];
}

void mergeSort(vector<int>& nums, int low, int high) {
    if (low >= high) return;
    int mid = low + (high - low) / 2;
    mergeSort(nums, low, mid);
    mergeSort(nums, mid + 1, high);
    merge(nums, low, mid, high);
}
Used in: count inversions, reverse pairs, sort linked list (05-linked-list/11-SortListMergeSort.md).


Quick sort: pick a pivot, put it in its correct place (smaller left, bigger right), recurse.
------------------------------------------------------------------------------------------
int partition(vector<int>& nums, int low, int high) {
    int pivot = nums[low], i = low, j = high;
    while (i < j) {
        while (i <= high - 1 && nums[i] <= pivot) i++;
        while (j >= low + 1 && nums[j] > pivot) j--;
        if (i < j) swap(nums[i], nums[j]);
    }
    swap(nums[low], nums[j]);
    return j;
}

void quickSort(vector<int>& nums, int low, int high) {
    if (low >= high) return;
    int p = partition(nums, low, high);
    quickSort(nums, low, p - 1);
    quickSort(nums, p + 1, high);
}
Worst case n^2 when the array is already sorted and pivot = first element -> pick a random pivot.
