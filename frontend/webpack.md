# Webpack for frontend and Vue developers

## What is webpack?

Webpack is a module bundler. It starts from one or more entry files, follows imports to build a dependency graph, transforms files when needed and emits browser-ready assets called bundles or chunks.

```text
entry file
   ↓
dependency graph from imports
   ↓
loaders transform modules
   ↓
plugins affect the build
   ↓
optimized output bundles/chunks
```

Example dependency graph:

```text
main.js
├── App.vue
│   ├── Header.vue
│   └── app.css
├── router.js
└── api.js
```

Webpack does not simply join files. It understands the relationships between modules and can split, optimize and load them differently.

## Should a new Vue project use webpack?

Vue currently recommends Vite for new applications. Vue CLI, which uses webpack, is in maintenance mode. You should still learn webpack when:

- maintaining Vue CLI or existing webpack applications;
- working with custom enterprise build pipelines;
- using webpack Module Federation;
- debugging bundle size and chunk-loading problems;
- interviewing for frontend roles involving established applications.

## Core concepts

### 1. Entry

The entry is where webpack begins constructing the dependency graph:

```javascript
export default {
  entry: "./src/main.js",
};
```

Webpack follows static and dynamic imports reachable from this entry.

### 2. Output

Output controls where and how generated files are emitted:

```javascript
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default {
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].[contenthash].js",
    chunkFilename: "[name].[contenthash].js",
    clean: true,
  },
};
```

- `[name]`: chunk name;
- `[contenthash]`: changes when file content changes;
- `chunkFilename`: naming for non-entry chunks;
- `clean`: remove old build output before emitting new output.

Content hashes support long-term browser caching.

### 3. Loaders

Loaders transform individual module types before bundling.

```javascript
module: {
  rules: [
    {
      test: /\.vue$/,
      use: "vue-loader",
    },
    {
      test: /\.css$/,
      use: ["style-loader", "css-loader"],
    },
  ],
}
```

- `test` selects matching files.
- `use` selects loaders.
- Loader chains execute from right to left.

For CSS above, `css-loader` understands CSS imports, then `style-loader` injects the result into the page.

For Vue Single-File Components, `vue-loader` processes `.vue` files and `VueLoaderPlugin` coordinates their template, script and style blocks.

### 4. Plugins

Plugins affect the broader compilation rather than transforming one file type.

```javascript
plugins: [
  new VueLoaderPlugin(),
  new HtmlWebpackPlugin({ template: "./public/index.html" }),
]
```

Common plugin responsibilities include HTML generation, environment values, CSS extraction, bundle analysis and Module Federation.

### 5. Mode

```javascript
export default {
  mode: "development",
};
```

- `development`: faster builds and debugging-friendly output;
- `production`: minification and production optimizations;
- `none`: no mode defaults.

Use production mode for production builds.

## A minimal Vue webpack configuration

```javascript
import path from "node:path";
import { fileURLToPath } from "node:url";
import HtmlWebpackPlugin from "html-webpack-plugin";
import { VueLoaderPlugin } from "vue-loader";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default {
  mode: "development",
  entry: "./src/main.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].[contenthash].js",
    clean: true,
  },
  module: {
    rules: [
      { test: /\.vue$/, use: "vue-loader" },
      { test: /\.css$/, use: ["style-loader", "css-loader"] },
      { test: /\.(png|jpg|svg)$/, type: "asset" },
    ],
  },
  resolve: {
    extensions: [".js", ".vue"],
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  plugins: [
    new VueLoaderPlugin(),
    new HtmlWebpackPlugin({ template: "./public/index.html" }),
  ],
  devServer: {
    historyApiFallback: true,
    hot: true,
  },
};
```

## Bundle versus chunk

A **module** is a source unit such as `App.vue` or `utils.js`.

A **chunk** is a group of modules created by webpack during compilation.

A **bundle** commonly means an emitted file sent to the browser. In everyday discussion, bundle and emitted chunk file are often used interchangeably.

```text
source modules → webpack chunks → emitted JavaScript files
```

## Why split bundles?

One large bundle has problems:

- slow initial download;
- more JavaScript to parse and execute;
- users download code for features they may never visit;
- changing application code may invalidate cached vendor code.

Code splitting produces smaller chunks that can be loaded initially, in parallel or on demand.

Webpack supports three main splitting approaches:

1. multiple entry points;
2. shared-chunk extraction with `SplitChunksPlugin`;
3. dynamic `import()`.

## 1. Multiple entry points

```javascript
entry: {
  main: "./src/main.js",
  admin: "./src/admin.js",
}
```

Webpack emits separate entry chunks such as `main.js` and `admin.js`.

This is useful for genuinely separate pages, but it is manual. Shared dependencies can be duplicated unless split-chunk configuration extracts them.

## 2. Dynamic imports: on-demand splitting

A static import is normally part of the current chunk graph:

```javascript
import AdminPage from "./AdminPage.vue";
```

A dynamic import creates an asynchronous chunk boundary:

```javascript
const AdminPage = () => import("./AdminPage.vue");
```

Webpack emits the admin code into another chunk. The browser downloads it only when the function runs.

### Vue Router lazy loading

```javascript
const routes = [
  {
    path: "/",
    component: () => import("./views/HomeView.vue"),
  },
  {
    path: "/admin",
    component: () => import("./views/AdminView.vue"),
  },
];
```

Initial navigation does not need the admin page. When the user visits `/admin`, webpack's runtime requests its chunk and then resolves the import promise.

This is **route-level code splitting**, usually the highest-value splitting strategy for a Vue SPA.

### Async Vue components

```javascript
import { defineAsyncComponent } from "vue";

const HeavyChart = defineAsyncComponent(
  () => import("./components/HeavyChart.vue"),
);
```

Use component-level splitting for large, conditionally displayed features. Splitting every small component creates too many requests and runtime overhead.

### Naming chunks

```javascript
const AdminPage = () =>
  import(
    /* webpackChunkName: "admin" */
    "./AdminPage.vue"
  );
```

Readable names help debugging. Content hashes still make filenames cache-safe.

## 3. `SplitChunksPlugin`

Webpack's `optimization.splitChunks` extracts modules shared between chunks or modules meeting cache-group rules.

```javascript
optimization: {
  splitChunks: {
    chunks: "all",
  },
  runtimeChunk: "single",
}
```

`chunks: "all"` allows optimization of both initial and async chunks.

Conceptual result:

```text
runtime.[hash].js   → webpack module/chunk loading runtime
vendors.[hash].js   → suitable node_modules dependencies
main.[hash].js      → application entry code
admin.[hash].js     → lazily loaded admin feature
```

The exact files depend on webpack's size and usage heuristics. Do not assume that every dependency automatically becomes one vendor file.

### Custom cache group

```javascript
optimization: {
  splitChunks: {
    chunks: "all",
    cacheGroups: {
      vueVendor: {
        test: /[\\/]node_modules[\\/](vue|vue-router|pinia)[\\/]/,
        name: "vue-vendor",
        priority: 20,
      },
    },
  },
}
```

Use custom groups only when measurements show a caching or loading benefit. Excessive manual splitting can make builds harder to maintain and create many small chunks.

## What happens when a lazy chunk loads?

```text
User visits /admin
      ↓
Vue Router runs import("./AdminView.vue")
      ↓
webpack runtime determines the chunk URL
      ↓
browser downloads that JavaScript file
      ↓
webpack registers/evaluates its modules
      ↓
import promise resolves
      ↓
Vue renders AdminView
```

If the file is missing or the network fails, the import promise rejects. Applications should show an error/retry experience for important lazy features.

## Prefetch and preload

Webpack magic comments can provide browser hints:

```javascript
import(
  /* webpackPrefetch: true */
  "./AdminView.vue"
);
```

- **prefetch**: download later during browser idle time because it may be needed in the future;
- **preload**: download with higher priority because it is expected during the current navigation.

Use them carefully. Prefetching too much defeats lazy loading, and preloading too much competes with critical resources.

## Tree shaking versus code splitting

They solve different problems:

- **tree shaking** removes unused exports from production output;
- **code splitting** moves used code into separate chunks loaded at different times.

Tree shaking works best with ES modules:

```javascript
import { usedFunction } from "./utilities.js";
```

The `sideEffects` field helps webpack safely remove unused modules:

```json
{
  "sideEffects": ["*.css"]
}
```

Do not mark every file side-effect-free if importing some files performs necessary setup or imports CSS.

## Browser caching

Use content hashes:

```javascript
filename: "[name].[contenthash].js"
```

A changed file receives a new name. Unchanged files keep their names and can remain cached.

Separating the webpack runtime can reduce unnecessary changes to application/vendor chunks:

```javascript
optimization: {
  runtimeChunk: "single",
}
```

Deployments must handle users running an older entry chunk that requests an older lazy chunk. Keep old hashed assets available for a period instead of deleting them immediately.

## Development source maps

```javascript
export default {
  devtool: "eval-cheap-module-source-map",
};
```

Source maps connect bundled code back to original source for debugging. Production source maps can help error monitoring but should be uploaded/served according to your security and deployment policy.

## Development server and HMR

Webpack Dev Server serves assets from memory during development. Hot Module Replacement updates changed modules without a complete page refresh where supported.

For history-mode Vue Router:

```javascript
devServer: {
  historyApiFallback: true,
}
```

This returns the SPA HTML for unknown navigation paths so refreshing `/orders/42` does not produce a server 404.

## Environment variables

Webpack replaces values at build time through plugins such as `DefinePlugin`:

```javascript
new webpack.DefinePlugin({
  __API_URL__: JSON.stringify(process.env.API_URL),
});
```

These values become part of browser JavaScript. Never place secrets in frontend environment variables; users can inspect the bundle.

## Measuring bundles

Do not optimize blindly. Inspect:

- initial JavaScript size;
- async chunk sizes;
- duplicate libraries;
- unused code;
- parse and execution time;
- loading waterfalls.

Useful tools include webpack stats, webpack-bundle-analyzer, browser network tools and performance profiling.

## Common problems

### Bundle is too large

- lazy-load routes and genuinely heavy features;
- inspect duplicate dependencies;
- remove or replace heavy libraries;
- import only required functionality;
- confirm production mode and tree shaking;
- analyze before creating custom split rules.

### Too many tiny chunks

Do not dynamically import every small component. Let webpack's split-chunk size rules combine suitable modules and split primarily at meaningful feature/route boundaries.

### Chunk load error after deployment

Usually an old page requests a chunk removed by a new deployment. Retain old content-hashed assets, reload gracefully when appropriate and avoid caching mutable HTML/manifest files forever.

### Works through navigation but refresh returns 404

Configure the production server to fall back to `index.html` for Vue Router history routes. `historyApiFallback` solves this only in the development server.

### Duplicate code across chunks

Inspect stats and ensure shared modules are eligible for `splitChunks`. Multiple package versions may prevent deduplication.

## Webpack versus Module Federation

Normal code splitting divides one build into chunks.

```text
one source/build → several chunks
```

Module Federation composes modules from separate builds at runtime.

```text
host build + independently deployed remote builds
```

Module Federation is useful for microfrontends. It is not required for normal route-level lazy loading.

## Interview questions

### What does webpack do?

It starts at entries, builds a dependency graph, transforms modules through loaders, applies plugins and emits optimized browser assets.

### Loader versus plugin?

A loader transforms matching modules. A plugin hooks into the broader compilation lifecycle for tasks such as HTML generation, asset extraction or federation.

### How does code splitting work?

Static imports are normally included in their current chunk graph. Dynamic `import()` creates an async chunk boundary. Webpack emits another file and its runtime downloads that file when the import executes. `SplitChunksPlugin` can extract shared modules and reduce duplication.

### Code splitting versus tree shaking?

Code splitting changes when code loads. Tree shaking removes code proven unused.

### Why use content hashes?

They allow immutable long-term caching. Only assets whose content changes receive new URLs.

### Best Vue splitting strategy?

Start with lazy-loaded routes. Split individual components only when they are heavy and not always rendered. Measure the result to avoid too many small chunks.

## Final revision

Remember this flow:

```text
entry
  ↓
dependency graph
  ↓
loaders transform modules
  ↓
plugins and optimization
  ↓
chunks with content hashes
  ↓
browser loads initial chunks
  ↓
dynamic imports load later chunks on demand
```
