# 3. Observer Pattern ⭐⭐⭐⭐⭐

One of the most important frontend patterns.

## Problem

When one thing changes, many other things should update automatically.

---

## Real World Example

Think of YouTube.

```
Creator uploads video
          │
          ▼
Subscribers receive notification
```

The creator doesn't notify everyone manually.

Subscribers observe the creator.

## Frontend Examples

### React

```
State changes
↓
Component re-renders
```

### Redux

```
Store changes
↓
Components update
```

### Vue

```
Reactive State
↓
UI updates
```

### RxJS

Also based on the Observer pattern.

---