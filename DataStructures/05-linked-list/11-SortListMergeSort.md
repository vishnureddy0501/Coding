# 11. Sort a Linked List with Merge Sort

LeetCode 148 — Sort List. This is an important revision problem.

Merge sort works well because a linked list can be split and merged by changing pointers.

```cpp
Node* merge(Node* first, Node* second) {
    Node dummy(-1);
    Node* tail = &dummy;

    while (first != nullptr && second != nullptr) {
        if (first->data <= second->data) {
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

Node* sortList(Node* head) {
    if (head == nullptr || head->next == nullptr) return head;

    // Find the first middle, not the second middle.
    Node* slow = head;
    Node* fast = head;
    while (fast->next != nullptr && fast->next->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }

    Node* rightHead = slow->next;
    slow->next = nullptr;

    Node* left = sortList(head);
    Node* right = sortList(rightHead);
    return merge(left, right);
}
```

The split must produce two non-empty smaller lists. Finding the first middle guarantees that for a two-node list.

Time: `O(n log n)`; recursion space: `O(log n)`.
