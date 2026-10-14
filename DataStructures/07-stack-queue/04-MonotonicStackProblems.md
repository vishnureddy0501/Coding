Monotonic stack: stack kept increasing (or decreasing). Finds next/previous smaller/greater
element for every index in O(n) total.

Next Greater Element template (traverse from right):
    stack<int> st;  vector<int> nge(n, -1);
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && st.top() <= nums[i]) st.pop();
        if (!st.empty()) nge[i] = st.top();
        st.push(nums[i]);
    }
Circular array (NGE II): loop i from 2n - 1 down to 0 and use nums[i % n].

907. Sum of Subarray Minimums
-----------------------------
for pse we have to keep < (lessthan)
for nse we have to keep <= (lessthan and equal to)

(or) vice versa

Leetcode Tapping rain water (still need to learn most-optimal)
84. Largest Rectangle in Histogram (still need to learn most-optimal)
85. Maximal Rectangle
402. Remove K Digits (still need to learn most-optimal)
239. Sliding Window Maximum (still need to learn most-optimal)
 The Celebrity Problem (naukari)
