# 8. Delete the Middle Node

Keep `slow` one node behind the usual middle pointer by delaying its first movement.

```cpp
Node* deleteMiddle(Node* head) {
    if (head == nullptr || head->next == nullptr) {
        delete head;
        return nullptr;
    }

    Node* slow = head;
    Node* fast = head->next->next;

    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }

    Node* middle = slow->next;
    slow->next = middle->next;
    delete middle;

    return head;
}
```

When the loop ends, `slow` points to the node immediately before the middle, so `slow->next` can be removed.
