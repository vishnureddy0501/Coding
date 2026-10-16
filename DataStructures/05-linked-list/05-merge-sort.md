# 5. Sort a Linked List

Use merge sort:

1. Find the first middle.
2. Split the list.
3. Sort both halves.
4. Merge them.

```cpp
ListNode* merge(ListNode* first, ListNode* second) {
    ListNode dummy(0);
    ListNode* tail = &dummy;

    while (first != nullptr && second != nullptr) {
        if (first->val <= second->val) {
            tail->next = first;
            first = first->next;
        } else {
            tail->next = second;
            second = second->next;
        }
        tail = tail->next;
    }

    tail->next = first != nullptr ? first : second;
    return dummy.next;
}

ListNode* sortList(ListNode* head) {
    if (head == nullptr || head->next == nullptr) return head;

    ListNode* slow = head;
    ListNode* fast = head->next;

    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }

    ListNode* rightHead = slow->next;
    slow->next = nullptr;

    ListNode* left = sortList(head);
    ListNode* right = sortList(rightHead);
    return merge(left, right);
}
```

Starting `fast` at `head->next` makes slow stop at the first middle, ensuring that both halves are smaller.

Time: `O(n log n)`; recursion space: `O(log n)`.
