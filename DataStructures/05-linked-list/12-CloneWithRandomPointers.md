# 12. Clone a Linked List with Random Pointers

Each node contains `next` and `random`. Clone the list in `O(1)` auxiliary space by temporarily placing each copy after its original.

## Step 1: Insert copied nodes

```text
A → B → C

becomes

A → A' → B → B' → C → C'
```

## Step 2: Connect random pointers

For an original node `current`, its copy is `current->next`.

```cpp
current->next->random =
    current->random == nullptr ? nullptr : current->random->next;
```

## Step 3: Separate both lists

```cpp
Node* copyRandomList(Node* head) {
    if (head == nullptr) return nullptr;

    for (Node* current = head; current != nullptr;) {
        Node* copy = new Node(current->data);
        copy->next = current->next;
        current->next = copy;
        current = copy->next;
    }

    for (Node* current = head; current != nullptr; current = current->next->next) {
        Node* copy = current->next;
        copy->random = current->random == nullptr
            ? nullptr
            : current->random->next;
    }

    Node* copiedHead = head->next;
    for (Node* current = head; current != nullptr;) {
        Node* copy = current->next;
        current->next = copy->next;
        copy->next = copy->next == nullptr ? nullptr : copy->next->next;
        current = current->next;
    }

    return copiedHead;
}
```

The separation step restores the original list, which must remain unchanged after cloning.

Time: `O(n)`; auxiliary space excluding copied nodes: `O(1)`.
