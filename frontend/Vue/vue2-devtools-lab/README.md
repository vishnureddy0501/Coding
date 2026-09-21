# Vue 2 DevTools Learning Lab

A JavaScript-only Vue 2 project designed to make important Vue DevTools behavior visible and repeatable.

## Run it

```bash
npm install
npm run serve
```

Open `http://localhost:8080`, then open browser DevTools and select the **Vue** tab.

## Labs

1. **Components** — inspect props, local state, computed values, and nested components.
2. **Props & events** — trace parent-child data flow and emitted payloads.
3. **Computed & watchers** — compare caching, template methods, and watcher side effects.
4. **Vuex** — follow actions, mutations, getters, and state changes.
5. **API timeline** — separate request time from frontend processing time.
6. **Rendering** — compare a large DOM with a small rendered window.
7. **Lifecycle** — observe mount/update/destroy hooks and cleanup.
8. **Debug challenges** — diagnose realistic symptoms using evidence.

## Suggested workflow

For every lab:

1. Read the DevTools task at the top.
2. Start a Vue Timeline or Chrome Performance recording.
3. Perform one interaction.
4. Stop recording and write down what changed.
5. Inspect relevant component state, props, computed values, events, or Vuex mutations.
6. Change one variable and repeat the recording.

The API and performance labs contain deliberately inefficient options for learning. They are clearly labelled in the interface and source.
