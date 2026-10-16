# 1. Basics and Dummy Node

## `ListNode` structure

```cpp
struct ListNode {
    int val;
    ListNode* next;

    ListNode() {
        val = 0;
        next = nullptr;
    }

    ListNode(int value) {
        val = value;
        next = nullptr;
    }

    ListNode(int value, ListNode* nextNode) {
        val = value;
        next = nextNode;
    }
};
```

## Traverse a list

```cpp
for (ListNode* current = head; current != nullptr; current = current->next) {
    cout << current->val << ' ';
}
```

## Why use a dummy node?

A dummy node is placed before the actual head. It avoids a separate case when the head itself changes.

```cpp
ListNode dummy(0, head);
ListNode* current = &dummy;

// Modify current->next as needed.

return dummy.next;
```

Use it for deletion, merging lists, and building a result list.

## Memory rule

If you remove a node created with `new`, save its address, reconnect the list, and then `delete` it.

```cpp
ListNode* removed = current->next;
current->next = removed->next;
delete removed;
```

This is enough memory-management knowledge for linked-list problems.
