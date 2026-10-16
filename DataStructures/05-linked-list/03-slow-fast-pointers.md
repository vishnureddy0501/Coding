# 3. Slow and Fast Pointers

Slow moves one step. Fast moves two steps.

## Second middle

Start both pointers at `head`.

```cpp
ListNode* secondMiddle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;

    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }

    return slow;
}
```

```text
Odd:  1 → 2 → 3          returns 2
Even: 1 → 2 → 3 → 4      returns 3
```

Use this for finding the normal middle node, such as LeetCode 876.

## First middle

Start `fast` one node ahead at `head->next`.

```cpp
ListNode* firstMiddle(ListNode* head) {
    if (head == nullptr) return nullptr;

    ListNode* slow = head;
    ListNode* fast = head->next;

    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }

    return slow;
}
```

```text
Odd:  1 → 2 → 3          returns 2
Even: 1 → 2 → 3 → 4      returns 2
```

Use the first middle when splitting a list for merge sort. It ensures that a two-node list is divided into two smaller one-node lists.

## Quick difference

```cpp
ListNode* fast = head;       // Second middle
ListNode* fast = head->next; // First middle
```

## Detect a cycle

```cpp
bool hasCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;

    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast) return true;
    }

    return false;
}
```

## Find the cycle starting point

First make slow and fast meet inside the cycle. Then move slow to the head and move both one step at a time.

```cpp
ListNode* detectCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;

    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast) {
            slow = head;

            while (slow != fast) {
                slow = slow->next;
                fast = fast->next;
            }

            return slow;
        }
    }

    return nullptr;
}
```

Time: `O(n)`; extra space: `O(1)`.
