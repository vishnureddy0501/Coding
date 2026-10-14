# 3. Memory Management

C++ does not have automatic garbage collection. Memory created with `new` must eventually be released with `delete`.

```cpp
Node* node = new Node(5);
delete node;
node = nullptr;
```

Deleting a pointer releases only that one object. It does not automatically delete the rest of the linked list.

## Delete the head

```cpp
Node* deleteHead(Node* head) {
    if (head == nullptr) return nullptr;

    Node* oldHead = head;
    head = head->next;
    delete oldHead;

    return head;
}
```

The caller must save the returned head:

```cpp
head = deleteHead(head);
```

Otherwise, the caller still holds a pointer to deleted memory.

## Delete the complete list

```cpp
void deleteList(Node*& head) {
    while (head != nullptr) {
        Node* nextNode = head->next;
        delete head;
        head = nextNode;
    }
}
```

## Important rules

- Use `delete` for memory created with `new`.
- Use `delete[]` for arrays created with `new[]`.
- Never access a node after deleting it.
- Avoid two owners deleting the same node.
- Local pointer variables disappear when a function returns, but heap nodes do not.
