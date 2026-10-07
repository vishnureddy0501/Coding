# Vendor and route-level code splitting

This document explains how JavaScript is split and loaded in this repository. It covers both development and production builds.

## The short version

There are two related, but different, kinds of splitting:

1. **Vendor splitting** is controlled by Webpack's `optimization.splitChunks.cacheGroups` in `webpack.dev.js` and `webpack.prod.js`. It moves third-party modules from `node_modules` into four `vendor-build-*` files.
2. **Route-level splitting** starts in `src/router/router.js`. A route component written as `() => import(...)` becomes an on-demand chunk. Vue Router calls that function when the route is entered, and Webpack's browser runtime downloads the chunk.

In simple terms:

```text
Initial page request
  -> HTML loads the entry files and initial vendor files
  -> Vue application starts
  -> user visits a lazy route
  -> Vue Router calls import(...)
  -> Webpack adds a <script> for that route chunk
  -> browser downloads it
  -> Vue renders the component
```

## 1. Where the build configuration lives

The build configuration is divided between these files:

| File | Responsibility |
| --- | --- |
| `webpack.common.js` | Entry points, output directory, loaders, aliases, plugins, and a fallback `vendor` cache group |
| `webpack.dev.js` | Development filenames, development public path, and the four development vendor groups |
| `webpack.prod.js` | Production hashed filenames, CDN/static public path, minification, manifest generation, and the same four vendor groups |
| `src/router/router.js` | Vue routes and most route-level dynamic imports |
| `package.json` | Commands that select the development or production Webpack configuration |

`webpack.dev.js` and `webpack.prod.js` are merged with `webpack.common.js`. Both mode-specific files explicitly disable the common file's single `vendor` group:

```js
cacheGroups: {
    default: false,
    defaultVendors: false,
    vendor: false,
    // vendorBundle1 ... vendorBundle4 follow
}
```

That is why the current builds produce `vendor-build-1` through `vendor-build-4`, rather than one `vendor.js` file.

## 2. How vendor code is split

Webpack creates a module graph by following imports from every entry in `webpack.common.js`, such as `app`, `meeting`, and `admin_landing`. The `splitChunks` rules then classify modules in that graph.

The current grouping is:

| Output chunk | What goes into it |
| --- | --- |
| `vendor-build-1` | Vue and UI packages: Vue, Vuex, Vue Router, Vuetify, Swiper, Quill-related Vue packages, and similar UI dependencies |
| `vendor-build-2` | Grid, chart, D3, Algolia, and search packages |
| `vendor-build-3` | Export/document/date/editor/image packages such as XLSX, jsPDF, JSZip, Moment, Day.js, docx, Tiptap, and html2canvas |
| `vendor-build-4` | The catch-all for any remaining module under `node_modules` |

The `test` regular expression decides whether a module belongs to a group. `priority` resolves overlaps: the higher-priority matching group wins. For example, Vue matches both the specific first group and the catch-all fourth group, but group 1 has priority `40`, so Vue goes into `vendor-build-1` instead of `vendor-build-4`.

Important details:

- Groups 1-3 use `chunks: 'initial'`. They classify dependencies used by an initial entry graph.
- Group 4 uses `chunks: 'all'`, so it can also extract third-party code reached through lazy imports.
- `enforce: true` tells Webpack to create the group even when its normal size/request heuristics might not do so.
- `maxInitialRequests: 10` limits the number of parallel initial chunk requests Webpack is allowed to create.
- `app-shared` collects application code used by at least four initial entry points. It is shared first-party code, not vendor code.
- `app-build-forecasts-deals` and `app-build-ai-collab` are first-party feature groups. Because they currently say `chunks: 'initial'`, they apply to initial chunks, not ordinary lazy-route chunks.

There is no hand-written `vendor.js` source file. These vendor files are generated build artifacts assembled from imported packages.

## 3. Development versus production vendor files

Both modes use the same four package groupings, so their logical chunk names match.

### Development

Run:

```bash
npm run build
```

or use watch/live reload with:

```bash
npm run dev
```

`webpack.dev.js` uses readable, stable names:

```text
vendor-build-1.js
vendor-build-2.js
app-dashboard.js
```

Its relevant settings are:

```js
output: {
    publicPath: '/dist/',
    filename: '[name].js',
    chunkFilename: '[name].js'
}
```

The repository's `npm run dev` command writes/watch-builds files and starts `live-server` on port 5500. The separate `dev-hot` command uses `webpack-dev-server` on port 9000. In both cases, the Webpack runtime uses the configured `publicPath` when it constructs a lazy chunk URL.

### Production

Run:

```bash
npm run build-prod
```

`webpack.prod.js` minifies the files and adds a content hash:

```text
vendor-build-1.<contenthash>.js
vendor-build-2.<contenthash>.js
app-dashboard.<contenthash>.js
```

Its relevant settings are:

```js
output: {
    publicPath: process.env.CDN_BASE_URL || '/static/js/dist/',
    filename: '[name].[contenthash].js',
    chunkFilename: '[name].[contenthash].js'
}
```

The hash changes when file content changes. This allows long browser caching without serving an old file after a deployment.

The production build also emits `manifest.json` through `WebpackManifestPlugin`. The manifest maps logical asset names/entry points to their hashed files. The server or deployment layer that renders the page can use that manifest to include the correct initial files. That server-side integration is outside this repository; this repository only generates the manifest.

For later, lazy requests, the already-loaded Webpack runtime knows the chunk ID, hashed filename, and `publicPath`. It therefore does not need the browser to read `manifest.json` for every route change.

If `CDN_BASE_URL` is provided during the production build, lazy chunks are requested from that CDN base. Otherwise they are requested below `/static/js/dist/`.

## 4. How route-level splitting is declared

Most lazy route components are declared near the top of `src/router/router.js`:

```js
const dashboardWrapper = () => import(
    /* webpackChunkName: "app-dashboard" */
    '../components/dashboard/DashboardWrapper.vue'
);
```

and then used normally in the route table:

```js
{
    path: '/some/path',
    component: dashboardWrapper
}
```

The difference between the two import styles is important:

```js
// Eager: included in the initial module graph.
import DashboardWrapper from '../components/dashboard/DashboardWrapper.vue';

// Lazy: creates an async boundary and returns a Promise.
const DashboardWrapper = () => import('../components/dashboard/DashboardWrapper.vue');
```

Vue Router accepts the second form as an async component factory. It does not call it while merely creating the route configuration. It calls it when that route must be rendered.

The `webpackChunkName` comment supplies a readable chunk name. Imports with the same name are intentionally grouped. For example, several dashboard route components use `app-dashboard`; they can therefore be delivered together instead of as one file per component.

Not every router dependency is lazy today. For example, `UserDemoRooms`, `NewLandingPage`, and `adminSettingsComponents` are statically imported at the top of `src/router/router.js`, so they and their statically imported dependency trees can contribute to the initial bundle. Convert a component only when delaying it is safe and useful.

## 5. What happens in the browser during navigation

Suppose the user opens a dashboard route whose component uses the `app-dashboard` chunk name.

1. A click or `router.push(...)` starts Vue Router navigation. A direct URL loaded for the first time also goes through route matching after the application starts.
2. Vue Router matches the URL and sees that the component is a function.
3. Vue Router calls the function, which executes `import(...)` and returns a Promise.
4. Webpack's runtime checks whether that chunk is already loaded.
5. If it is not loaded, the runtime creates a script request using `output.publicPath` plus the generated chunk filename. Extracted lazy CSS can also be requested as a separate CSS chunk.
6. After the script registers its modules, the Promise resolves and Vue Router renders the component.
7. If another route uses the same named chunk, the browser/runtime reuses the already-loaded chunk; it is not downloaded again.

Example request names:

```text
Development: /dist/app-dashboard.js
Production:  /static/js/dist/app-dashboard.<contenthash>.js
CDN prod:    <CDN_BASE_URL>/app-dashboard.<contenthash>.js
```

The application does not contain a manual `fetch()` or Axios call for these JavaScript chunks. The `import()` expression is transformed by Webpack, and Webpack's small runtime performs the script loading automatically.

On a hard refresh of a nested route, the web server must first return the application's HTML rather than a 404. After the app starts, Vue Router matches the URL and triggers the same lazy chunk request. That HTML/history fallback is a server concern, separate from Webpack splitting.

## 6. How to make a new route lazy

Assume a new page lives at `src/components/orders/OrdersView.vue`.

First, declare it as a dynamic import in `src/router/router.js`:

```js
const OrdersView = () => import(
    /* webpackChunkName: "app-orders" */
    '../components/orders/OrdersView.vue'
);
```

Then use it in the route:

```js
{
    path: '/welcome/home/orders',
    name: 'orders',
    component: OrdersView
}
```

Guidelines for the chunk name:

- Use a stable, feature-based name such as `app-orders`.
- Give closely related routes the same name when they are normally used together.
- Give a large, rarely visited screen its own name when loading it separately improves the initial page.
- Do not include a content hash in the magic comment; the production filename template adds it.

Everything imported normally by `OrdersView.vue` becomes part of its async dependency graph. A dependency may instead be extracted into a shared/vendor chunk when a matching `splitChunks` rule applies.

## 7. How to add or move a vendor package

Usually no change is needed. Any package under `node_modules` falls into `vendor-build-4` automatically.

If a package should join a specific group, update the matching `test` expression in **both** `webpack.dev.js` and `webpack.prod.js`. Keeping the two files aligned prevents local and production builds from having unexpectedly different chunk layouts.

For example, to place a hypothetical `new-chart-lib` package in group 2, add it to that group's package alternatives:

```js
vendorBundle2: {
    test: /[\\/]node_modules[\\/](...|new-chart-lib)[\\/]/,
    name: 'vendor-build-2',
    priority: 35,
    chunks: 'initial'
}
```

Before moving a package, consider the trade-off. A vendor file that changes less often caches well, but putting too much into one file makes users download more code up front. A package used only by one lazy feature may be better left in that feature's async graph or in an async shared vendor chunk.

## 8. How to verify the result

After changing the configuration or a route import:

1. Run `npm run build` for development behavior and/or `npm run build-prod` for production behavior.
2. Inspect `static/js/dist/` for the expected chunk name. Production files should contain hashes.
3. In production output, inspect `static/js/dist/manifest.json` for initial entry assets and generated file mappings.
4. Open browser DevTools, select the Network tab, filter by JS, and reload the initial page.
5. Confirm that the route chunk is absent initially, then navigate to the route and confirm that it is requested.
6. Navigate away and back. The same file should normally be served from memory/disk cache rather than downloaded again.

If the chunk request returns 404, check `output.publicPath`, `CDN_BASE_URL`, whether the built files were deployed under that base, and whether the page is using assets from the same release. If the route code appears in the initial bundle, look for a static import of that component (or of an index file that re-exports it) elsewhere in the initial graph.

## 9. A useful mental model

Think of the application as luggage:

- Entry chunks are the bag carried onto every initial page.
- Vendor chunks are shared bags containing third-party libraries.
- Route chunks are bags delivered only when the user visits that feature.
- `webpackChunkName` is the label on a route bag.
- `publicPath` tells the browser where the baggage room is.
- A production content hash is the version printed on the label.
- `manifest.json` tells the page-rendering/deployment side which hashed initial bags belong to each entry.

The two main places to remember are therefore:

```text
Vendor grouping: webpack.dev.js + webpack.prod.js
Route splitting: src/router/router.js using () => import(...)
```
