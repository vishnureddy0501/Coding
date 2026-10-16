# 2. Reverse a Linked List

Keep three pointers:

```text
previous ← current    next
```

Before changing `current->next`, save the original next node.

```cpp
ListNode* reverseList(ListNode* head) {
    ListNode* previous = nullptr;
    ListNode* current = head;

    while (current != nullptr) {
        ListNode* nextNode = current->next;
        current->next = previous;

        previous = current;
        current = nextNode;
    }

    return previous;
}
```

Time: `O(n)`; extra space: `O(1)`.

This is the most important linked-list snippet.
