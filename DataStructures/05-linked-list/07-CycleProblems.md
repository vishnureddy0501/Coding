# 7. Cycle and Intersection Problems

## Intersection of two linked lists

```cpp
Node* getIntersectionNode(Node* headA, Node* headB) {
    Node* first = headA;
    Node* second = headB;

    while (first != second) {
        first = first == nullptr ? headB : first->next;
        second = second == nullptr ? headA : second->next;
    }

    return first;
}
```

Each pointer travels `lengthA + lengthB`, so they align at the intersection. If there is no intersection, both become `nullptr`.

## Detect whether a cycle exists

Use slow and fast pointers. If they meet, a cycle exists. If fast reaches `nullptr`, no cycle exists.

## Find the cycle length

After slow and fast meet, keep one pointer fixed and move the other until it returns to the meeting node. Count the steps.

```cpp
int cycleLength(Node* meetingNode) {
    int length = 1;
    Node* current = meetingNode->next;

    while (current != meetingNode) {
        ++length;
        current = current->next;
    }

    return length;
}
```

For the cycle starting node, use the complete [Floyd template](06-CycleStartTemplate.md).
