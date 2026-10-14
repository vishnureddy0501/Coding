# 4. Doubly Linked List

Each node points both forward and backward.

```text
null ← [prev | 10 | next] ⇄ [prev | 20 | next] → null
```

## Reverse a doubly linked list

Swap the meaning of `next` and `prev` for every node.

```cpp
Node* reverseDLL(Node* head) {
    if (head == nullptr || head->next == nullptr) return head;

    Node* previous = nullptr;
    Node* current = head;

    while (current != nullptr) {
        Node* nextNode = current->next;

        current->next = previous;
        current->prev = nextNode;

        previous = current;
        current = nextNode;
    }

    return previous;
}
```

Time: `O(n)`; extra space: `O(1)`.
