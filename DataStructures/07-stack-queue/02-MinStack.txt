Min stack in O(1) extra space (encoding trick).
Use long long: 2 * x - minVal overflows int.
Simpler O(n) space version: stack of pairs {value, minSoFar}.

Variables:
	stack: regular stack to store modified values.
	minVal: variable to store the current minimum.

push(x):
	If stack is empty:
		Push x
		Set minVal = x
	If x >= minVal:
		Push x
	If x < minVal:
		Push 2*x - minVal (encoded value)
		Update minVal = x

pop():
	If top >= minVal:
		Just pop
	If top < minVal:
		This means the top is an encoded value
		To restore previous minVal:
		minVal = 2*minVal - top
		Then pop
top():
	If top >= minVal:
		Return top
	Else:
		Return minVal (actual value was encoded)

getMin():
	Return minVal