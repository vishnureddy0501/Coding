# React Design Patterns Roadmap

## Estimated Time

**25–35 Hours**

---

## By the End You'll Understand

- Custom Hooks
- Container / Presentational Pattern
- Provider Pattern
- Compound Components
- Controlled vs Uncontrolled Components
- Higher Order Components (HOC)
- Render Props
- State Reducer Pattern
- Props Getter Pattern
- Slot Pattern

---

# Pattern Priority

| Priority | Pattern | Common Usage |
|-----------|----------|--------------|
| ⭐⭐⭐⭐⭐ | Custom Hooks | Every React app |
| ⭐⭐⭐⭐⭐ | Container / Presentational | API separation |
| ⭐⭐⭐⭐⭐ | Provider Pattern | Context API |
| ⭐⭐⭐⭐⭐ | Compound Components | UI libraries |
| ⭐⭐⭐⭐ | Controlled / Uncontrolled Components | Forms |
| ⭐⭐⭐⭐ | Render Props | Older React codebases |
| ⭐⭐⭐⭐ | Higher Order Components (HOC) | Legacy projects |
| ⭐⭐⭐ | State Reducer Pattern | Headless UI |
| ⭐⭐⭐ | Props Getter Pattern | Component libraries |
| ⭐⭐⭐ | Slot Pattern | Component composition |

---

# 1. Custom Hook Pattern ⭐⭐⭐⭐⭐

## Problem

Suppose three different pages need to fetch users.

Without a custom hook, every page repeats the same logic.

```jsx
useEffect(() => {
    fetchUsers();
}, []);
```

### Page A

```jsx
useEffect(() => {
    fetchUsers();
}, []);
```

### Page B

```jsx
useEffect(() => {
    fetchUsers();
}, []);
```

### Page C

```jsx
useEffect(() => {
    fetchUsers();
}, []);
```

Lots of duplicated code.

---

## Solution

Move the logic into a reusable hook.

```jsx
function useUsers() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        fetchUsers().then(setUsers);
    }, []);

    return users;
}
```

Now every page simply does:

```jsx
const users = useUsers();
```

Done.

---

## Visualization

### Without Custom Hook

```
Page A
   │
 Fetch Users

Page B
   │
 Fetch Users

Page C
   │
 Fetch Users
```

### With Custom Hook

```
Page A
      │
Page B ├── useUsers()
      │
Page C
```

One place to maintain.

---

## Real Examples

```jsx
useUsers()

useProducts()

useAuth()

useTheme()

usePagination()

useDebounce()
```

---

# 2. Container / Presentational Pattern ⭐⭐⭐⭐⭐

## Problem

One component is responsible for everything.

```jsx
function UserCard() {

    fetchUsers();

    // loading

    // error

    // render UI
}
```

It:

- Fetches data
- Handles loading
- Handles errors
- Renders UI

Everything is mixed together.

---

## Solution

Split responsibilities.

### Container Component

Responsible for:

- Fetching data
- Business logic
- State

```jsx
function UserContainer() {

    const users = useUsers();

    return <UserList users={users} />;
}
```

### Presentational Component

Responsible only for UI.

```jsx
function UserList({ users }) {

    return (
        ...
    );
}
```

`UserList` doesn't know APIs exist.

It simply renders.

---

## Visualization

```
UserContainer

      │

Fetch Data

      │

Pass Props

      │

UserList

      │

Render UI
```

---

# 3. Provider Pattern ⭐⭐⭐⭐⭐

Used by React Context.

---

## Problem

Suppose every component needs the logged-in user.

Without Context:

```
App

↓

Home

↓

Dashboard

↓

Profile

↓

Navbar
```

You keep passing `user` as props.

This is **Prop Drilling**.

---

## Solution

Create a Provider.

```
UserProvider

↓

All Components
```

Now any component can access the user.

```jsx
const user = useContext(UserContext);
```

No prop drilling.

---

## Common Examples

- ThemeProvider
- RouterProvider
- Redux Provider
- QueryClientProvider

All use the **Provider Pattern**.

---

# 4. Compound Components ⭐⭐⭐⭐⭐

Very common in UI libraries.

---

Instead of this:

```jsx
<Modal
    title="Delete"
    footer="Cancel"
/>
```

Write this:

```jsx
<Modal>
    <Modal.Header />
    <Modal.Body />
    <Modal.Footer />
</Modal>
```

Much more flexible.

---

## Another Example

```jsx
<Tabs>

    <Tabs.List />

    <Tabs.Trigger />

    <Tabs.Content />

</Tabs>
```

Libraries using this pattern:

- Radix UI
- Headless UI
- shadcn/ui
- Material UI

---

# 5. Controlled vs Uncontrolled Components ⭐⭐⭐⭐

## Controlled Component

React owns the value.

```jsx
<input
    value={name}
    onChange={handleChange}
/>
```

The input value always comes from React state.

---

## Uncontrolled Component

The DOM owns the value.

```jsx
<input
    ref={inputRef}
/>
```

You read the value later using the ref.

---

## Rule

Most React forms use **Controlled Components**.

---

# 6. Higher Order Component (HOC) ⭐⭐⭐⭐

A popular pattern before Hooks.

---

## Problem

Many pages require authentication.

Instead of adding authentication logic everywhere:

```
Dashboard

↓

Check Login

Profile

↓

Check Login

Settings

↓

Check Login
```

---

## Solution

Wrap the component.

```jsx
export default withAuth(Dashboard);
```

Now `withAuth` handles authentication.

The component only focuses on rendering.

---

## Visualization

```
Dashboard

↓

withAuth

↓

Export
```

Still common in older React projects.

---

# 7. Render Props ⭐⭐⭐⭐

Popular before Hooks.

Instead of:

```jsx
<DataLoader />
```

Use:

```jsx
<DataLoader>
    {(data) => (
        <Users data={data} />
    )}
</DataLoader>
```

The child is a function.

Nowadays this pattern is mostly replaced by **Custom Hooks**.

---

# 8. State Reducer Pattern ⭐⭐⭐

Common in headless UI libraries.

Normally the component decides everything.

With this pattern:

Users can override internal behavior.

Libraries like **Downshift** use this approach.

Rare in business applications.

---

# 9. Props Getter Pattern ⭐⭐⭐

Libraries return helper props.

Example:

```jsx
const {
    getInputProps
} = useSearch();
```

Usage:

```jsx
<input
    {...getInputProps()}
/>
```

Very common in headless component libraries.

---

# 10. Slot Pattern ⭐⭐⭐

Instead of:

```jsx
<Card
    header="..."
    footer="..."
/>
```

Use:

```jsx
<Card>

    <Header />

    <Body />

    <Footer />

</Card>
```

React children act as slots.

Very common in reusable component libraries.

---

# Patterns You're Probably Already Using

| Technology | Pattern |
|------------|----------|
| React Query | Custom Hook |
| Context API | Provider |
| Redux | Provider |
| shadcn/ui | Compound Components |
| React Hook Form | Controlled / Uncontrolled |

---

# Real Project Structure

```
src/

hooks/
    useUsers.js

providers/
    AuthProvider.jsx

containers/
    UsersContainer.jsx

components/
    UserCard.jsx
    UserList.jsx

pages/
    Users.jsx
```

Each folder represents a common React design pattern.

---

# Interview Priority

## Must Know

- ✅ Custom Hooks
- ✅ Provider Pattern
- ✅ Compound Components
- ✅ Controlled vs Uncontrolled Components
- ✅ Container / Presentational Pattern

---

## Good to Know

- Higher Order Components (HOC)
- Render Props
- Slot Pattern

---

## Nice to Know

- State Reducer Pattern
- Props Getter Pattern

---

# Recommended Learning Order

Don't try to learn every pattern at once.

Instead, follow this order:

1. Custom Hook Pattern ⭐⭐⭐⭐⭐
2. Container / Presentational Pattern ⭐⭐⭐⭐⭐
3. Provider Pattern ⭐⭐⭐⭐⭐
4. Compound Components ⭐⭐⭐⭐⭐
5. Controlled vs Uncontrolled Components ⭐⭐⭐⭐
6. Higher Order Components (HOC) ⭐⭐⭐⭐
7. Render Props ⭐⭐⭐⭐
8. State Reducer Pattern ⭐⭐⭐
9. Props Getter Pattern ⭐⭐⭐
10. Slot Pattern ⭐⭐⭐

This progression closely matches how these patterns appear in real-world React applications and frontend interviews.