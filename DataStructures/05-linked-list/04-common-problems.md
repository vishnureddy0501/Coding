# 4. Common Interview Problems

## Delete the nth node from the end

Keep a gap of `n` nodes between fast and slow. The dummy node handles deleting the head.

```cpp
ListNode* removeNthFromEnd(ListNode* head, int n) {
    ListNode dummy(0, head);
    ListNode* slow = &dummy;
    ListNode* fast = &dummy;

    for (int i = 0; i < n; ++i) {
        fast = fast->next;
    }

    while (fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next;
    }

    ListNode* removed = slow->next;
    slow->next = removed->next;
    delete removed;

    return dummy.next;
}
```

## Intersection of two lists

When a pointer reaches the end, move it to the other list's head.

```cpp
ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
    ListNode* first = headA;
    ListNode* second = headB;

    while (first != second) {
        first = first == nullptr ? headB : first->next;
        second = second == nullptr ? headA : second->next;
    }

    return first;
}
```

Both pointers travel the same total distance: `lengthA + lengthB`.

## Check whether a list is a palindrome

Find the end of the first half, reverse only the second half, and compare.

```cpp
bool isPalindrome(ListNode* head) {
    if (head == nullptr || head->next == nullptr) return true;

    ListNode* slow = head;
    ListNode* fast = head;

    // slow stops at the end of the first half.
    while (fast->next != nullptr && fast->next->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }

    ListNode* secondHalf = reverseList(slow->next);
    ListNode* firstHalf = head;
    ListNode* current = secondHalf;
    bool palindrome = true;

    while (current != nullptr) {
        if (firstHalf->val != current->val) {
            palindrome = false;
            break;
        }

        firstHalf = firstHalf->next;
        current = current->next;
    }

    // Restore the original list.
    slow->next = reverseList(secondHalf);

    return palindrome;
}
```

### Odd number of nodes

```text
1 → 2 → 3 → 2 → 1
        ↑
       slow

First half used for comparison:  1 → 2
Middle node ignored:             3
Reversed second half:            1 → 2
```

### Even number of nodes

```text
1 → 2 → 2 → 1
    ↑
   slow

First half:            1 → 2
Reversed second half:  1 → 2
```

Only the second half is reversed by calling `reverseList(slow->next)`. The loop compares nodes only until the shorter second half ends, so the middle node in an odd-length list is ignored.
