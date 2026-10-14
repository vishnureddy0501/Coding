# 6. Floyd's Cycle Detection

Floyd's algorithm uses slow and fast pointers without extra memory.

## Detect a cycle and find its starting node

```cpp
Node* detectCycle(Node* head) {
    Node* slow = head;
    Node* fast = head;

    // Phase 1: find a meeting point inside the cycle.
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast) {
            // Phase 2: find the cycle entry.
            slow = head;

            while (slow != fast) {
                slow = slow->next;
                fast = fast->next;
            }

            return slow;
        }
    }

    return nullptr;
}
```

After the first meeting, the distance from the head to the cycle entry equals the forward distance from the meeting point to the entry, modulo the cycle length. Moving both pointers one step makes them meet at the entry.

The same idea is used in LeetCode 287, Find the Duplicate Number, where `next(index) = nums[index]`.
