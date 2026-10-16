# 6. Clone a List with Random Pointers

## Hash-map solution

```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        unordered_map<Node*, Node*> originalToCopy;
        Node* dummyNode = new Node(-1);
        Node* copiedCurrent = dummyNode;
        Node* originalCurrent = head;

        while (originalCurrent != nullptr) {
            Node* copiedNode = new Node(originalCurrent->val);
            originalToCopy[originalCurrent] = copiedNode;
            copiedCurrent->next = copiedNode;
            copiedCurrent = copiedCurrent->next;
            originalCurrent = originalCurrent->next;
        }

        originalCurrent = head;
        copiedCurrent = dummyNode->next;

        while (originalCurrent != nullptr) {
            copiedCurrent->random = originalToCopy[originalCurrent->random];
            originalCurrent = originalCurrent->next;
            copiedCurrent = copiedCurrent->next;
        }

        Node* copiedHead = dummyNode->next;
        delete dummyNode;
        return copiedHead;
    }
};
```

Time: `O(n)`; extra space: `O(n)` for the map.

## Space-optimized approach

The problem can also be solved without a map in `O(1)` auxiliary space by:

1. inserting every copied node after its original node;
2. connecting copied random pointers;
3. separating the original and copied lists.

The hash-map solution is easier to understand and write during an interview. Learn the no-map approach only if the interviewer asks for constant extra space.
