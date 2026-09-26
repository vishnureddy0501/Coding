# Frontend Performance — Quick Interview Notes

## Scenario

> The API returns in one second, but the UI takes more than five seconds to display. How do you debug it?

## First thing I check

Open **Chrome DevTools → Network** and confirm:

- When did the request start?
- When did the response finish?
- What is the response size?
- Are there duplicate or sequential requests?

The backend may take one second, but the request itself might start late. Always check the complete browser timeline.

```text
Request starts late
    → Check routing, authentication, JavaScript, or dependent APIs

Response arrives quickly but UI appears late
    → Check frontend processing and rendering
```

---

## Debugging flow

```text
1. Network panel
        ↓
2. Response size
        ↓
3. Data processing
        ↓
4. Component rendering
        ↓
5. Layout and paint
        ↓
6. Fix and measure again
```

---

## 1. Network panel

| Observation | Likely problem |
|---|---|
| Request starts late | Frontend logic is delaying it |
| High TTFB | Backend or network is slow |
| Large download time | Response is too large |
| Same API called multiple times | Watcher/lifecycle issue |
| APIs run one after another | Unnecessary sequential calls |
| Response completes but UI is blank | Processing or rendering issue |

Independent APIs should run in parallel:

```js
const [users, accounts] = await Promise.all([
  fetchUsers(),
  fetchAccounts()
]);
```

---

## 2. Response size

A fast API can still return thousands of records. The browser must parse, process, make them reactive, and create DOM elements.

Fixes:

- Server-side pagination
- Server-side filtering and sorting
- Return only required fields
- Load summary first and details later
- Compress the response

---

## 3. Data processing

Measure expensive transformations:

```js
console.time('transform');
const result = transformData(response.data);
console.timeEnd('transform');
```

Look for:

- Nested loops
- Repeated `filter`, `sort`, or `find`
- Date formatting for thousands of rows
- Transformations repeated during every render

Use a lookup map instead of calling `find()` repeatedly:

```js
const accountMap = new Map(
  accounts.map(account => [account.id, account])
);

const result = users.map(user => ({
  ...user,
  account: accountMap.get(user.accountId)
}));
```

---

## 4. Vue rendering

Use **Vue DevTools → Performance** and Chrome's **Performance** panel.

Check for:

- Components rendering repeatedly
- Deep watchers
- Expensive methods called from templates
- State updates inside large loops
- Unstable `:key` values
- Huge tables rendered at once

Prefer computed properties for derived data:

```js
computed: {
  activeUsers() {
    return this.users.filter(user => user.active);
  }
}
```

Avoid doing this directly in the template:

```vue
<UserRow
  v-for="user in users.filter(user => user.active)"
  :key="user.id"
/>
```

---

## 5. Large tables and lists

Rendering 10,000 rows creates too many DOM elements.

Fixes:

- Pagination
- Virtual scrolling
- Render only visible rows
- Lazy-load expanded details
- Avoid mounting hidden tabs until opened

---

## 6. JavaScript and browser work

Use Chrome's **Performance** panel and record the slow action.

Look for:

- Long JavaScript tasks
- Excessive component updates
- Large layout or paint time
- Heavy chart initialization
- Large script bundles

Fixes:

- Lazy-load routes and heavy components
- Split large bundles
- Load charts only when visible
- Move very heavy calculations to a Web Worker
- Reduce DOM size and layout changes

---

## Vue DevTools workflow

1. Open Vue DevTools.
2. Go to the **Performance** tab.
3. Start recording.
4. Perform the slow action.
5. Stop recording.
6. Find components that render many times or take too long.
7. Inspect their props, state, computed properties, and watchers.
8. Fix the cause and record again.

Vue DevTools shows **which component** is slow. Chrome Performance shows whether the browser spends time in **JavaScript, layout, or paint**.

---

## Common problem → solution

| Problem | Solution |
|---|---|
| Large API response | Pagination and fewer fields |
| Duplicate API calls | Fix watcher/lifecycle logic |
| Sequential requests | `Promise.all()` |
| Expensive transformations | Cache results and improve algorithm |
| Too many rows | Virtual scrolling or pagination |
| Repeated Vue renders | Narrow reactive dependencies |
| Heavy charts | Lazy rendering |
| Large bundle | Code splitting and lazy loading |

---

## Interview answer

> First, I check the Network panel to confirm when the request starts, when it finishes, its response size, and whether there are duplicate or sequential requests.
>
> If the response arrives in one second but the UI takes another four seconds, the problem is in frontend processing or rendering. I record the action using Chrome Performance and Vue DevTools. I look for expensive transformations, repeated component renders, large tables, long JavaScript tasks, and layout or paint work.
>
> Based on the measurement, I apply a targeted fix such as pagination, virtual scrolling, optimized transformations, fewer state updates, parallel API calls, or lazy loading. Finally, I record the same action again and compare the before-and-after timings.

## Short answer

> First check the Network panel. If the response arrives quickly, profile the gap between response completion and UI rendering using Chrome Performance and Vue DevTools. Find whether the time is spent in data processing, repeated renders, DOM creation, layout, or painting, fix that specific bottleneck, and measure again.

## Remember

```text
Measure → Find the bottleneck → Fix → Measure again
```
