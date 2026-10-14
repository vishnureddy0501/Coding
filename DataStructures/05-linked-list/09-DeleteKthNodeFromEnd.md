# 9. Delete the Kth Node from the End

Use a dummy node so deleting the head does not require a separate case.

```cpp
Node* removeNthFromEnd(Node* head, int k) {
    Node dummy(0, head);
    Node* slow = &dummy;
    Node* fast = &dummy;

    for (int step = 0; step < k; ++step) {
        fast = fast->next;
    }

    while (fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next;
    }

    Node* removed = slow->next;
    slow->next = removed->next;
    delete removed;

    return dummy.next;
}
```

After creating a gap of `k` nodes, moving both pointers keeps that gap unchanged. When fast reaches the end, slow is immediately before the node to delete.

Assumption: `1 <= k <= list length`.
