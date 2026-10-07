# Webpack — simple explanation

## What is Webpack?

Webpack is a tool that prepares frontend code so a browser can run it.

While developing, we write many different files:

- JavaScript files
- Vue components
- CSS and SCSS files
- Images and fonts
- Third-party packages

A browser cannot directly use all these files in their development form. Webpack reads them, processes them, and creates browser-ready files.

Think of Webpack like a packing department:

~~~text
Source code written by developers
        ↓
Webpack reads and processes it
        ↓
Optimized files are created
        ↓
Browser downloads and runs those files
~~~

## Why do we need Webpack?

Webpack solves a few important problems.

### 1. It understands imports

Our files import other files. Those files may import even more files.

Webpack starts from an entry file, follows all imports, and builds a complete map of what the application needs.

index.js (entry point) -> follows imports -> creates dependency graph.

### 2. It compiles Vue files

This repository uses Vue single-file components. A Vue file can contain:

- HTML-like templates
- JavaScript
- CSS or SCSS

Browsers do not understand Vue files directly. Webpack converts them into normal browser JavaScript and styles.

### 3. It compiles modern JavaScript

The project uses modern JavaScript features. Webpack works with Babel to convert supported modern syntax into code suitable for the browsers targeted by the project.

### 4. It compiles SCSS

Browsers understand CSS but not SCSS. Webpack uses Sass-related loaders to convert SCSS into CSS.

### 5. It handles images and fonts

Webpack can:

- place a small image directly inside generated code;
- create a separate file for a large image;

### 6. It improves loading performance

Webpack can divide the application into smaller files.

The browser initially downloads only the files needed to start the page. Other files can be downloaded later when the user opens a feature.

## The basic Webpack flow

~~~text
1. Start from an entry file
2. Follow its imports
3. Process each type of file
4. Divide code into useful groups
5. Optimize the result
6. Write browser-ready files into the output folder
~~~

## Important Webpack terms

### Entry

An entry is the first source file Webpack starts reading.

For example, the main application starts from **src/index.js**.

Webpack follows every import reachable from that file.

### Output

Output is where Webpack writes the generated files.

In this repository, generated files go to:

~~~text
static/js/dist
~~~

### Loader

Helps webpack to process files.

A loader teaches Webpack how to process a particular file type.

Examples:

| Loader | Purpose |
|---|---|
| vue-loader | Processes Vue components |
| babel-loader | Processes JavaScript |
| sass-loader | Converts Sass/SCSS into CSS |
| css-loader | Resolves CSS imports and asset URLs |
| vue-style-loader | Adds component styles to the page |
| url-loader | Inlines small images or fonts |
| file-loader | Emits an asset as a separate file |

### Chunk

A chunk is one part of the built application.

Instead of creating one extremely large JavaScript file, Webpack creates multiple chunks. The browser can load some immediately and others later.

### Public path

The public path tells the browser where generated files are hosted.

Locally, files come from the local server. In production, they can come from the CDN.

## How Webpack is organized in this repository

There are three main configuration files.

### webpack.common.js

This contains settings shared by development and production:

- application entry points;
- output directory;
- loaders;
- import aliases;
- common plugins;
- common chunk settings.

### webpack.dev.js

This contains development settings:

- readable filenames such as app.js;
- local public paths;
- source maps for debugging;
- Webpack development server;
- watch and development chunk settings.

### webpack.prod.js

This contains production settings:

- optimized and minimized JavaScript;
- CDN paths;
- production chunk splitting;
- manifest generation;

- removal of unused Moment locales.
- content-hashed filenames;


## Why does this repository have multiple entries?

This repository builds several browser pages and applications.

Important entries include:

- **app:** the main application;
- **admin_landing:** the Admin microfrontend host;
- **onboarding:** the onboarding host;

Each entry has a different starting file.

This prevents every page from loading the entire main application.

For example, the Admin landing page can start from **admin_landing.js** without starting **index.js**, which belongs to the main application.

## Simple example: building the main application

Suppose Webpack starts from **src/index.js**.

That file imports the root Vue component, router, store, plugins, and other modules. Those files import more components and styles.

Webpack follows the chain:

~~~text
src/index.js
   ├── application component
   ├── router
   ├── Vuex store
   ├── translations
   ├── CSS/SCSS
   └── other imported components and libraries
~~~

Webpack processes everything and creates files such as:

~~~text
app.js
vendor-build-1.js
vendor-build-2.js
app-shared.js
feature chunks
~~~

In production, names include hashes:

~~~text
app.abc123.js
vendor-build-1.def456.js
~~~

## What is code splitting?

The application contains many large features. Users do not need every feature as soon as the first page opens.

Routes therefore use dynamic imports. For example, Dashboard code can be placed in an **app-dashboard** chunk.

The behavior is:

~~~text
User opens application
        ↓
Browser loads initial application files
        ↓
User opens Dashboard
        ↓
Browser downloads the Dashboard chunk
        ↓
Dashboard is rendered
~~~

This is called lazy loading.

It improves the initial page load because feature code is downloaded only when needed.

### Where is the lazy chunk downloaded from?

- **Locally:** it is downloaded from the local development server.
- **In production:** Webpack creates the chunk in **static/js/dist**. The deployment pipeline uploads it to **S3**, and the browser downloads it through the **CDN URL**.

Webpack uses its configured **publicPath** to create the chunk URL automatically.

~~~text
User opens Dashboard
        ↓
Webpack requests app-dashboard.<hash>.js from the CDN
        ↓
CDN returns the chunk stored in S3
        ↓
Dashboard is rendered
~~~

## What are vendor chunks?

**Vendor** means code written by outside libraries, not code written by our application team.

For example:

- Vue
- Vue Router
- Lodash
- Moment
- Chart.js
- AG Grid

These packages are installed inside **node_modules**.

Our own components, pages, and business logic are called **application code**. Code imported from node_modules is usually called **vendor code**.

~~~text
Application code:
Our Dashboard, Deals, Forecasts, and Admin components

Vendor code:
Vue, Lodash, Moment, Chart.js, AG Grid, and other libraries
~~~

A **vendor chunk** is simply a separate JavaScript file containing some of those third-party libraries.

Instead of putting everything into one large file:

~~~text
app.js
  ├── our application code
  ├── Vue
  ├── charts
  ├── grids
  └── all other libraries
~~~

Webpack separates them:

~~~text
app.js                 → our application code
vendor-build-1.js      → Vue and UI libraries
vendor-build-2.js      → charts, grids, and search libraries
vendor-build-3.js      → document, date, and editor libraries
vendor-build-4.js      → remaining third-party libraries
~~~

### Why separate vendor code?

Third-party libraries usually change less often than our application code.

Suppose we update one Dashboard component:

- The application bundle changes.
- The vendor bundles may stay unchanged.
- The browser downloads the new application bundle.
- It can reuse vendor bundles from its cache.

This can reduce repeat downloads.

Separating vendor code also prevents this large repository from producing one extremely large vendor file. The four groups make the files easier for the build process to optimize and help avoid memory problems during production minification.

### Does the browser always load every vendor chunk?

It loads the vendor chunks required by the current application entry or feature. Webpack records which chunks are dependencies and the backend includes the initial ones. Lazy feature chunks can request other required chunks later.


### Which images does Webpack process?

Webpack processes an image when that image becomes part of its dependency graph.


### What about images in the static folder?

It depends on how they are used:

- If application code or imported CSS imports/resolves a file from **static**, Webpack processes that reference.
- If the page uses a plain URL such as **/static/images/logo.svg**, Webpack does not process that file as part of the JavaScript graph. The deployment pipeline copies the static directory separately.


### Which fonts does this mean?
        webpack process only local fonts present in the repository.
        it cannot access dynamic fonts coming from backend. because webpack runs at compile time. not run time.

### What does Webpack do with imported files?

small files: store in code directly.
large files: stored in dist/ folder along with output. and those are served separately.

Small files can avoid an extra network request. Large files remain separate so they do not make the JavaScript unnecessarily large and can be cached independently.

## What are content-hashed filenames?

In production, Webpack adds a short code called a **hash** to each filename:

~~~text
app.js  →  app.7a81c9.js
~~~

The hash is based on the file's content.

- If the file does not change, its name stays the same and the browser uses its cached copy.
- If the file changes, it gets a new name and the browser downloads the new version.

We need this to prevent users from running old cached JavaScript after a deployment.

## What is the manifest?

The process happens before the browser requests the JavaScript:

1. Webpack builds the frontend.
2. It creates a file such as **app.7a81c9.js**.
3. It writes that filename into the manifest.
4. When a user opens the website, the browser first requests the HTML page from the backend.
5. The backend reads the manifest and puts the actual hashed filename into the HTML.
6. The browser sees that filename and requests it directly.

For example, the manifest tells the backend:

~~~text
app.js → app.7a81c9.js
~~~

The backend then produces HTML similar to:

~~~html
<script src="https://cdn.example.com/app.7a81c9.js"></script>
~~~

The browser reads this HTML and directly downloads:

~~~text
app.7a81c9.js
~~~

~~~text
Webpack build
    ↓
Creates app.7a81c9.js and manifest
    ↓
Browser asks backend for the HTML page
    ↓
Backend reads manifest
    ↓
Backend puts app.7a81c9.js in the HTML
    ↓
Browser requests app.7a81c9.js from the CDN
~~~

The manifest can also tell the backend which vendor and shared files belong to an entry. This allows the backend to include all files needed to start that page.

In simple terms:

> The manifest is a build-generated lookup file used by the backend while creating HTML. The browser does not use the manifest directly. It receives the correct hashed script URL inside the HTML and requests that URL from the CDN.

## How does the CDN work with Webpack?

Webpack writes files into **static/js/dist** during the build.

In production, the GitHub Actions workflow uploads that complete directory to a release-specific path in the production **aviso-ui-bundles-prod** S3 bucket. Non-production uses the **aviso-ui-bundles** bucket. The browser-facing location is supplied through **CDN_BASE_URL**.

Webpack's public path tells the browser the CDN location:

~~~text
Build-machine location:
static/js/dist/app.abc123.js

Browser location:
https://cdn.example.com/.../static/js/dist/app.abc123.js
~~~

The correct public path is especially important for lazy-loaded chunks. When the user opens a feature, Webpack combines that path with the generated chunk filename to create the CDN request URL.

If the path is wrong, the first page may load successfully but later navigation can fail with a ChunkLoadError.

## Development build versus production build

### Development

The development build focuses on developer convenience:

- stable and readable filenames;
- quicker rebuilding;
- file watching;
- local server support;
- source maps for debugging;
- no heavy production minification.

### Production

The production build focuses on users:

- smaller JavaScript;
- content-hashed filenames;
- CDN-compatible URLs;
- optimized chunks;
- generated manifest for the backend.

## Webpack and the Admin microfrontend

Webpack creates the **admin_landing** host bundle from **src/admin_landing.js**.

That bundle starts a small Vue 2 application. At runtime, that application downloads the independent Admin UMD microfrontend from the CDN.

These are two separate stages:

~~~text
Build time:
Webpack builds the admin_landing host

Runtime:
The admin_landing host downloads the remote Admin microfrontend
~~~

Webpack in this repository does not use Module Federation. The Admin remote is loaded with a normal script at runtime.

## One-sentence answer

> Webpack takes our Vue 2 source code and assets, converts them into browser-ready files, divides them for efficient loading, optimizes them for production, and connects the generated CDN files to the backend through a manifest.

## Five points to remember

If you forget everything else, remember:

1. Webpack starts from entry files and follows imports.
2. Loaders process Vue, JavaScript, SCSS, images, and fonts.
3. It creates initial, shared, vendor, and lazy-loaded chunks.
4. Production uses hashes and CDN paths for performance and caching.
5. The manifest tells the backend which generated files to load.




Not Needed for now:
------------------
## Common problems


### Image works locally but not in production

Check:

- generated image URL;
- CDN path;
- whether the asset was uploaded;
- whether the asset belongs to static files or Webpack output.

### ChunkLoadError

This normally means the browser could not download a lazy chunk.

Possible causes:

- incorrect public path;
- chunk was not uploaded;
- backend and CDN are using different releases;
- stale browser or CDN cache.
