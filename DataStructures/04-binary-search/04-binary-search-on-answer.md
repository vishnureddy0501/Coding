# 4. Binary search on the answer

Use this when:

1. the possible answer is within a numeric range;
2. you can test a candidate answer;
3. the test is monotonic.

## Minimum possible answer

```cpp
long long minimumPossible(long long low, long long high) {
    long long answer = -1;

    while (low <= high) {
        long long mid = low + (high - low) / 2;

        if (isPossible(mid)) {
            answer = mid;
            high = mid - 1; // Success: try a smaller answer.
        } else {
            low = mid + 1;
        }
    }

    return answer;
}
```

Used by Koko Eating Bananas, Minimum Days for Bouquets, Ship Packages, Book Allocation, and Split Array Largest Sum.

## Maximum possible answer

```cpp
long long maximumPossible(long long low, long long high) {
    long long answer = -1;

    while (low <= high) {
        long long mid = low + (high - low) / 2;

        if (isPossible(mid)) {
            answer = mid;
            low = mid + 1; // Success: try a larger answer.
        } else {
            high = mid - 1;
        }
    }

    return answer;
}
```

Used by Aggressive Cows and Magnetic Force Between Two Balls.

## How to choose the range

Choose the tightest obviously correct bounds.

Examples:

| Problem | Low | High |
|---|---:|---:|
| Koko Eating Bananas | 1 | maximum pile |
| Ship Packages in D Days | maximum weight | sum of weights |
| Split Array Largest Sum | maximum element | sum of elements |
| Aggressive Cows | 0 | last position − first position |

Tighter bounds mean fewer iterations.

## Example: Koko Eating Bananas

```cpp
long long hoursNeeded(const vector<int>& piles, int speed) {
    long long hours = 0;
    for (int pile : piles) {
        hours += (pile + speed - 1LL) / speed; // ceil(pile / speed)
    }
    return hours;
}

int minEatingSpeed(vector<int>& piles, int h) {
    int low = 1;
    int high = *max_element(piles.begin(), piles.end());
    int answer = high;

    while (low <= high) {
        int speed = low + (high - low) / 2;

        if (hoursNeeded(piles, speed) <= h) {
            answer = speed;
            high = speed - 1;
        } else {
            low = speed + 1;
        }
    }

    return answer;
}
```

The pattern is:

```text
slow speeds: impossible
fast speeds: possible
find the first possible speed
```

## Integer nth root with overflow protection

Avoid directly calculating `mid^n`; it may overflow.

```cpp
// -1: value < target, 0: equal, 1: value > target
int comparePower(long long base, int exponent, long long target) {
    long long product = 1;

    for (int i = 0; i < exponent; ++i) {
        if (product > target / base) return 1;
        product *= base;
    }

    if (product == target) return 0;
    return -1;
}

long long nthRoot(int n, long long value) {
    if (value == 0) return 0;

    long long low = 1;
    long long high = value;

    while (low <= high) {
        long long mid = low + (high - low) / 2;
        int comparison = comparePower(mid, n, value);

        if (comparison == 0) return mid;
        if (comparison < 0) low = mid + 1;
        else high = mid - 1;
    }

    return -1;
}
```

`product > target / base` checks whether the next multiplication would exceed the target without performing an overflowing multiplication.

## Kth missing positive number

At index `mid`, the count of missing positive numbers before `nums[mid]` is:

```text
missing = nums[mid] - (mid + 1)
```

```cpp
int findKthPositive(vector<int>& nums, int k) {
    int low = 0;
    int high = nums.size() - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;
        int missing = nums[mid] - (mid + 1);

        if (missing < k) low = mid + 1;
        else high = mid - 1;
    }

    return low + k;
}
```

This is worth deriving with pen and paper instead of memorizing.
