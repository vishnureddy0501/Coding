# 5. String DP

For two strings, the common state is:

```text
dp[i][j] = answer using the first i characters of text1
           and the first j characters of text2
```

Using lengths instead of direct indices makes empty-string base cases easy.

## Longest Common Subsequence

```cpp
int longestCommonSubsequence(string text1, string text2) {
    int n = text1.size();
    int m = text2.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));

    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (text1[i - 1] == text2[j - 1]) {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    return dp[n][m];
}
```

## Print the LCS

Build the same table, then walk backward.

```cpp
string buildLCS(string& text1, string& text2, vector<vector<int>>& dp) {
    int i = text1.size();
    int j = text2.size();
    string answer;

    while (i > 0 && j > 0) {
        if (text1[i - 1] == text2[j - 1]) {
            answer.push_back(text1[i - 1]);
            --i;
            --j;
        } else if (dp[i - 1][j] >= dp[i][j - 1]) {
            --i;
        } else {
            --j;
        }
    }

    reverse(answer.begin(), answer.end());
    return answer;
}
```

## Problems derived from LCS

| Problem | Useful relation |
|---|---|
| Longest Palindromic Subsequence | LCS of string and reversed string |
| Minimum insertions for palindrome | `n - LPS` |
| Delete operations for two strings | `n + m - 2 × LCS` |
| Shortest Common Supersequence length | `n + m - LCS` |

Other essential string DP problems are Edit Distance, Distinct Subsequences, and Wildcard Matching.
