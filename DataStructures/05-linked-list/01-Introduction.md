# 1. Introduction

A linked list contains nodes connected through pointers.

```text
head
 ↓
[10 | next] → [20 | next] → [30 | null]
```

## Complexity

| Operation | Complexity |
|---|---:|
| Access the kth element | `O(k)` |
| Search by value | `O(n)` |
| Insert/delete after a known node | `O(1)` |
| Insert/delete when the node must first be found | `O(n)` |

Unlike an array, a linked list does not support random access.

## Dummy-node pattern

A dummy node is a temporary node placed before the result list. It removes special handling for the first inserted node.

```cpp
Node* dummy = new Node(-1);
Node* tail = dummy;

while (/* nodes remain */) {
    tail->next = new Node(value);
    tail = tail->next;
}

Node* result = dummy->next;
delete dummy;
return result;
```

Use it for problems such as:

- Add Two Numbers;
- merge two sorted lists;
- partition a list;
- delete a node when the head might change.

See [Memory Management](03-MemoryManagement.md) for correct use of `new` and `delete`.
