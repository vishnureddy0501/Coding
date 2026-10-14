# 2. Singly Linked List

Each node stores a value and a pointer to the next node.

```cpp
class Node {
public:
    int data;
    Node* next;

    Node(int value, Node* nextNode) {
        data = value;
        next = nextNode;
    }

    explicit Node(int value) {
        data = value;
        next = nullptr;
    }
};
```

It can also be written more compactly:

```cpp
struct Node {
    int data;
    Node* next;

    explicit Node(int value, Node* nextNode = nullptr)
        : data(value), next(nextNode) {}
};
```

## Creating nodes

```cpp
Node* first = new Node(10);
Node* second = new Node(20);
first->next = second;

Node* head = first;
```

`head` points to the first node. The last node's `next` is `nullptr`.
