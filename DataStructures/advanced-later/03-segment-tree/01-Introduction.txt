Range Query Data Structure
--------------------------
 Segment Tree
	Min/ Max Range Query
	Point Updates
	Sum Range Query
	Point Update

Lazy Propogation in Segment Tree
Coin related problem
Fenwick Tree / Binary Indexed Tree.


Segment Trees:
--------------
root ->          index i
root->left       index (2*i) + 1
root->right      index (2*i) + 2


eg: [1, 10, 40, 4, -10]
queries: [[1, 3], [0, 1], [0, 3]]...
find the minimum value in each range. (in this type of questions we use Segment trees)


we will take [l, r] from queries and traverse in tree.

parital overlap of node with range (l, r):
----------------------------------------
// tree node [nodeLeft, nodeRight] 
// some values in [nodeLeft, nodeRight] are not present in [l, r];
return min(left, right);   // for sum queries: left + right

no overlap:
-----------
no intersection

return INT_MAX; (because we are trying to find minimum value, INT_MAX never wins a min)
                  (sum query -> return 0, max query -> return INT_MIN)

complete overlap:
-----------------
[nodeLeft, nodeRight] is completely present in [l, r];

return seg[idx];