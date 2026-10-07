### Plugin

A **plugin** is an extra tool that performs a task during the Webpack build.

Webpack can create bundles by itself, but real projects also need tasks such as:

- making files smaller;
- creating a list of generated files;
- adding environment values;
- creating CSS files;
- generating source maps;
- analyzing bundle size.

Plugins perform these build-level tasks.

### Loader versus plugin

This is the easiest way to remember the difference:

> A loader processes a particular type of source file. A plugin performs a task for the overall build.

For example:

~~~text
sass-loader
    ↓
Processes each SCSS file

TerserPlugin
    ↓
Minifies the JavaScript produced by the complete production build
~~~

Think of a loader as a worker assigned to one type of material. Think of a plugin as a manager performing a job across the whole packaging process.

### Why do we need plugins?

The basic Webpack bundle is not enough for production. We need smaller files, correct environment configuration, cache-friendly output, debugging support, and information that other systems can use.

Plugins automate these tasks and run them at the correct stage of the build.

### Common Webpack plugins

These are common across Webpack projects:

| Plugin | Simple purpose | Why it is needed |
|---|---|---|
| HtmlWebpackPlugin | Creates an HTML file and adds generated script tags | Generated filenames can change, especially when hashes are used |
| MiniCssExtractPlugin | Creates separate CSS files | CSS can be downloaded and cached separately from JavaScript |
| DefinePlugin | Adds compile-time values such as environment settings | The same source can behave differently in development and production |
| TerserPlugin | Minifies JavaScript | Smaller JavaScript downloads faster |
| CopyWebpackPlugin | Copies files without bundling them | Useful for public files that should be copied as they are |
| BundleAnalyzerPlugin | Shows what is inside each bundle | Helps find large dependencies and duplicated code |

Not every project needs every plugin.

### Plugins used in this repository

#### VueLoaderPlugin

Works with vue-loader so Webpack can correctly compile Vue single-file components.

#### VuetifyLoaderPlugin

Supports the repository's Vuetify component and style processing.

#### DefinePlugin

Adds values while the application is being built.

In this repository, it provides the static CDN base URL and sets production mode. Application code can use the value without hardcoding a different URL for every environment.

It must not contain secrets because the value becomes part of browser code.

#### TerserPlugin

Makes production JavaScript smaller by removing unnecessary formatting and shortening generated code. This reduces download size.

#### WebpackManifestPlugin

Creates a manifest describing the generated files.

Production filenames contain hashes, for example:

~~~text
app.a1b2c3.js
~~~

The backend uses the manifest to find the correct filename instead of guessing the hash.

#### IgnorePlugin

Prevents selected modules from entering the bundle.

This repository excludes unused Moment.js locale files, reducing bundle size.

#### BundleAnalyzerPlugin

Can create a visual report showing how much space each package uses. It helps developers understand why a bundle is large. It is configured here but disabled by default.

#### SourceMapDevToolPlugin

Creates development source maps. Source maps connect generated bundle lines back to the original source files, making browser debugging easier.

#### ProvidePlugin

Automatically provides a dependency when code expects a global variable. This repository uses it for Quill in development.

#### LodashModuleReplacementPlugin

Builds a smaller Lodash version containing only the enabled feature types needed by this project.

#### MiniCssExtractPlugin

This plugin is configured in the repository. Normally it creates separate CSS files, but it also requires its loader in the style rules. The inspected rules currently use vue-style-loader, so do not claim that component CSS extraction is definitely active without checking the actual build output.

### Simple definition to remember

> A Webpack plugin performs a build-level task, such as minifying JavaScript, injecting environment settings, creating a manifest, or analyzing bundle size. We need plugins to turn a basic bundle into production-ready output.
