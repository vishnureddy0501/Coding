key points:
----------
✅ Factory = function returning object
✅ Use closures for private state
✅ Prefer factories over classes in JS



# 2. Factory Pattern

## What Problem Does It Solve?

Imagine you're building an application where users can have different roles.

Initially, you only have two roles:

- Admin
- User

A beginner might write code like this everywhere.

```javascript
// Login Page
let user;

if (type === "admin") {
    user = {
        role: "admin",
        permissions: ["ALL"]
    };
} else {
    user = {
        role: "user",
        permissions: ["READ"]
    };
}
```

Later...

Another developer needs the same logic in Dashboard.js

Later...

Another page same logic
Now imagine six months later.
Your company introduces a new role: SUPER_ADMIN

Now you must update **every single place** where this logic exists.

```
Login ❌
Dashboard ❌
Profile ❌
Settings ❌
Reports ❌
Analytics ❌
```

Problems:

- Duplicate code
- Hard to maintain
- Easy to forget one place
- Bugs happen when different pages create users differently

---

## Solution — Factory Pattern

Move the object creation into **one place**.

```javascript
function createUser(type) {
    switch (type) {
        case "admin":
            return {
                role: "admin",
                permissions: ["ALL"]
            };

        case "user":
            return {
                role: "user",
                permissions: ["READ"]
            };

        default:
            throw new Error("Invalid user type");
    }
}
```

Now, everywhere else in your application, you simply call the factory.

```javascript
const admin = createUser("admin");

const user = createUser("user");
```

Notice something important:

The rest of the application **doesn't know how users are created.**

It simply asks:

> "Give me an Admin."

The factory decides what to return.

---

## Why Is This Better?

    Suppose your company introduces a new role.
    Instead of changing 20 files...
    You only change one place
---

---

## Frontend Example 2 — Button Factory

Suppose your application has three button styles.

- Primary
- Secondary
- Danger

Instead of creating them manually everywhere...

```javascript
<Button color="blue" />

<Button color="red" />

<Button color="gray" />
```

Create a factory.

```javascript
function createButton(type) {
    switch (type) {
        case "primary":
            return <Button color="blue" />;

        case "secondary":
            return <Button color="gray" />;

        case "danger":
            return <Button color="red" />;
    }
}
```

Usage:

```javascript
createButton("primary");

createButton("danger");
```

---

## Interview Definition

**Factory Pattern is a creational design pattern that centralizes object creation into a single place. Instead of creating objects throughout the application, we ask the factory to create them. This reduces duplicate code, improves maintainability, and makes it easier to add new object types in the future.**

---

## How to Identify a Factory Pattern

Ask yourself:

> **"Am I creating similar objects in multiple places?"**

If the answer is **yes**, it's often a good candidate for a Factory Pattern.




utils.js
--------
const createUser = ({ id, name, role }) => {
  return {
    id,
    name,
    role,
    canEdit() {
      return role === "admin";
    }
  };
};

usage: 
------
const user = createUser({ id: 1, name: "Vishnu", role: "admin" });
