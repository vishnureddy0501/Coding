# 2. Longest-Window Problems

## Longest substring without repeating characters

```cpp
int lengthOfLongestSubstring(string text) {
    vector<int> frequency(256, 0);
    int left = 0;
    int answer = 0;

    for (int right = 0; right < text.size(); ++right) {
        ++frequency[text[right]];

        while (frequency[text[right]] > 1) {
            --frequency[text[left]];
            ++left;
        }

        answer = max(answer, right - left + 1);
    }

    return answer;
}
```

## Max consecutive ones after flipping at most `k` zeroes

```cpp
int longestOnes(vector<int>& nums, int k) {
    int left = 0;
    int zeroes = 0;
    int answer = 0;

    for (int right = 0; right < nums.size(); ++right) {
        if (nums[right] == 0) ++zeroes;

        while (zeroes > k) {
            if (nums[left] == 0) --zeroes;
            ++left;
        }

        answer = max(answer, right - left + 1);
    }

    return answer;
}
```

## At most `k` distinct values

```cpp
int longestAtMostKDistinct(vector<int>& nums, int k) {
    unordered_map<int, int> frequency;
    int left = 0;
    int answer = 0;

    for (int right = 0; right < nums.size(); ++right) {
        ++frequency[nums[right]];

        while (frequency.size() > k) {
            --frequency[nums[left]];
            if (frequency[nums[left]] == 0) frequency.erase(nums[left]);
            ++left;
        }

        answer = max(answer, right - left + 1);
    }

    return answer;
}
```

Fruit Into Baskets is the same pattern with `k = 2`.
