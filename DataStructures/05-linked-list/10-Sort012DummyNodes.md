# 10. Sort a Linked List of 0s, 1s, and 2s

Create three temporary lists and join them. Dummy nodes keep the code clean even when one group is empty.

```cpp
Node* sortList(Node* head) {
    Node zeroDummy(-1);
    Node oneDummy(-1);
    Node twoDummy(-1);

    Node* zeroTail = &zeroDummy;
    Node* oneTail = &oneDummy;
    Node* twoTail = &twoDummy;

    while (head != nullptr) {
        Node* nextNode = head->next;
        head->next = nullptr;

        if (head->data == 0) {
            zeroTail->next = head;
            zeroTail = head;
        } else if (head->data == 1) {
            oneTail->next = head;
            oneTail = head;
        } else {
            twoTail->next = head;
            twoTail = head;
        }

        head = nextNode;
    }

    oneTail->next = twoDummy.next;
    zeroTail->next = oneDummy.next != nullptr ? oneDummy.next : twoDummy.next;

    return zeroDummy.next;
}
```

This rearranges existing nodes instead of creating new data nodes.

Time: `O(n)`; extra space: `O(1)`.
