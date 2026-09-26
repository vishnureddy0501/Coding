stack using queue:
-------------------

algorithm:
---------
	push: 
		insert to queue.
		take n-1 elements from start & insert at back

	top: q.front();
	pop: q.pop();

code:
------
#include <queue>
using namespace std;

class Stack {
    queue<int> q;
public:
    void push(int val) {
        q.push(val);
        int n = q.size();
        for (int i = 0; i < n - 1; i++) {
            q.push(q.front());
            q.pop();
        }
    }

    int pop() {
        if (q.empty()) return -1;
        int topVal = q.front();
        q.pop();
        return topVal;
    }

    int top() {
        if (q.empty()) return -1;
        return q.front();
    }

    bool empty() {
        return q.empty();
    }
};



queue using 2 stack:
------------------
approach 1: (push costly)
------------
push:
	move all elements from s1 -> s2
	push x to s1
	move all elements from s2 to s1
delete from queue: 
	s1.pop();
front of queue:
	s1.top();


approach 2 for queue using 2 stacks:
-------------------------------------
push: directly push to stack.
pop: 
	if s2 is empty then copy elements from s1 to s2.
	if s2 is not empty the take the top of stack.
	if s2 is empty then return -1

top: 
	if s2 is empty then copy elements from s1 to s2.
	if s2 is not empty the take the top of stack.
	if s2 is empty then return -1

 empty: 
    return s1.empty() && s2.empty()
