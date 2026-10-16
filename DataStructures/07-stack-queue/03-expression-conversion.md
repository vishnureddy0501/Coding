# 3. Expression Conversion

## Operator precedence

```cpp
int priority(char operation) {
    if (operation == '^') return 3;
    if (operation == '*' || operation == '/') return 2;
    if (operation == '+' || operation == '-') return 1;
    return 0;
}
```

## Infix to postfix

```cpp
string infixToPostfix(string expression) {
    stack<char> operations;
    string result;

    for (char token : expression) {
        if (isalnum(token)) {
            result += token;
        } else if (token == '(') {
            operations.push(token);
        } else if (token == ')') {
            while (!operations.empty() && operations.top() != '(') {
                result += operations.top();
                operations.pop();
            }
            operations.pop();
        } else {
            while (!operations.empty() && operations.top() != '(' &&
                   (priority(operations.top()) > priority(token) ||
                    (priority(operations.top()) == priority(token) && token != '^'))) {
                result += operations.top();
                operations.pop();
            }

            operations.push(token);
        }
    }

    while (!operations.empty()) {
        result += operations.top();
        operations.pop();
    }

    return result;
}
```

`^` is right-associative, so an equal-priority `^` is not popped.

## Postfix to infix

For an operator, pop right operand first and left operand second.

```cpp
string postfixToInfix(string expression) {
    stack<string> values;

    for (char token : expression) {
        if (isalnum(token)) {
            values.push(string(1, token));
        } else {
            string right = values.top();
            values.pop();

            string left = values.top();
            values.pop();

            values.push("(" + left + token + right + ")");
        }
    }

    return values.top();
}
```

Remember:

```text
Postfix traversal: left operator right
Prefix conversion: traverse from right to left
```
