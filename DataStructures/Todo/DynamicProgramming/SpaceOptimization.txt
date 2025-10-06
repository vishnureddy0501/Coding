Instead of 2 dimentional array use curr, prev for space optimization
--------------------------------------------------------------------
how to do the space optimization:
---------------------------------
suppose you are using 2d array in problems like 0/1 knapsack.
we can achive the result using 2 single dimentional arrays curr, prev.
Hence this way we can reduce the space taken.


class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        int n = coins.size();
        sort(coins.begin(), coins.end());
        vector<int> prev(amount+1, INT_MAX), curr(amount+1, INT_MAX);
        curr[0] = 0;
        for (int j = 0; j <= amount; j++) {
            curr[j] = ((j %coins[0]) == 0 )? (j / coins[0]) : INT_MAX;
        }
        prev = curr;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j <= amount; j++) {
                if (j - coins[i] >= 0 && curr[j-coins[i]] != INT_MAX) {
                    curr[j] = min(prev[j], curr[j-coins[i]] + 1);
                } else {
                    curr[j] = prev[j];
                }
            }
            prev = curr;
        }
        return curr[amount] == INT_MAX ? -1 : curr[amount];
    }
};