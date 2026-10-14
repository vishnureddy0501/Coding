# 5. Slow and Fast Pointers

The slow pointer moves one step while the fast pointer moves two.

## Find the middle

```cpp
Node* middleNode(Node* head) {
    Node* slow = head;
    Node* fast = head;

    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }

    return slow;
}
```

- Odd number of nodes: returns the exact middle.
- Even number of nodes: returns the second middle.

## Find the first middle

Merge sort needs the first middle so that both resulting lists contain at least one node.

```cpp
Node* firstMiddle(Node* head) {
    Node* slow = head;
    Node* fast = head;

    while (fast->next != nullptr && fast->next->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }

    return slow;
}
```
