# How I implemented the Admin microfrontend

## Interview opening answer

> I implemented the Admin experience using a runtime-loaded microfrontend architecture. The existing product was a Vue 2 application, so I kept a small Vue 2 host entry called **admin_landing**. The host owns page bootstrap, authentication context, the shared Vuex store, API configuration, and translations. The actual Admin UI is built and deployed independently as a UMD bundle on our CDN. At runtime, the host selects the correct CDN URL, downloads the bundle, installs it as a Vue plugin, and renders the global component registered by that plugin. This lets the Admin team release independently while still using the product's session, state, APIs, and translations.

## The problem I was solving

The product is a large Vue 2 application. Building every Admin feature directly into it would mean:

- Admin releases are tied to the main application's release cycle.
- The main bundle grows even for users who never visit Admin.
- Team ownership and release responsibility are less clear.
- An Admin dependency or build problem can affect the full application.

I separated the feature into a remotely deployed frontend while retaining a thin integration layer in the main application.

## Architecture

~~~text
                         Build time

 Main UI repository                         Remote Admin repository
 ┌─────────────────────────┐                ┌──────────────────────────┐
 │ Vue 2 host entry        │                │ Admin Vue 2 application  │
 │ Shared store and i18n   │                │ Components and workflows │
 │ Runtime module loader   │                │ Vue plugin entry         │
 └────────────┬────────────┘                └─────────────┬────────────┘
              │                                           │
              │ Webpack build                             │ UMD build
              ▼                                           ▼
       Host application                         Versioned CDN bundle
                                            ui-self-serve-onboarding.umd.js


                         Runtime

 Browser opens Admin page
          │
          ▼
 Backend page loads the admin_landing host bundle
          │
          ▼
 Host mounts on its DOM element
          │
          ▼
 Host chooses the environment-specific remote URL
          │
          ▼
 Browser downloads the remote UMD script
          │
          ▼
 Script exposes window.UiSelfServeOnboarding
          │
          ▼
 Host installs it as a Vue plugin and passes dependencies
          │
          ▼
 Plugin globally registers SelfServeOnboardingApp
          │
          ▼
 Host renders the Admin experience
~~~

## Responsibility boundary

### The host owns

- The page and DOM mount point.
- Deciding when and from where to load the remote.
- The authenticated browser session.
- The existing Vue 2 runtime.
- Shared Vuex state.
- API endpoint configuration.
- Internationalization.
- The loading and failure states.
- The contract used to install the remote.

### The remote owns

- Admin screens and workflows.
- Feature components and presentation.
- Feature-specific state.
- Registering its root component during installation.
- Consuming only the dependencies exposed by the host contract.
- Producing an independently deployable UMD artifact.

The host handles integration; the remote handles the feature.

## How the host is built

The main repository has multiple Webpack entries. **admin_landing** is a separate entry from the main application.

The production build creates:

- A content-hashed admin_landing JavaScript bundle.
- Any shared vendor/application chunks required by that entry.
- A Webpack manifest mapping the logical entry to its generated files.

The backend page uses that manifest to include the correct assets and supplies the DOM element on which the Vue host mounts.

The separate entry means the Admin page does not need to start the entire main SPA. It starts only the shell needed to load the Admin microfrontend.

## How the remote is built

The remote is built as a **UMD library**, rather than a normal application that owns an HTML page.

Its build contract conceptually contains:

- Library/global name: **UiSelfServeOnboarding**.
- A plugin entry exporting an install function.
- Root component: **SelfServeOnboardingApp**.
- Vue configured as a peer/external dependency.
- Static assets configured to resolve from the CDN.
- Production optimization and versioned output.

UMD works well here because the browser can load it with an ordinary script tag. After evaluation, it publishes a predictable global that the host can discover. This approach does not require Module Federation.

## Vue-version compatibility

The current host uses Vue 2.7.16 and installs the remote into the host's Vue constructor. Therefore, the existing remote contract must be **Vue 2-compatible**.

The remote should normally use Vue as an external or peer dependency rather than packaging another Vue runtime. Sharing the host runtime ensures:

- The remote registers components in the same component registry used by the host.
- Plugin installation uses the same Vue constructor.
- Vuex and i18n integrations are compatible.
- Duplicate runtime and reactivity problems are avoided.

A standard Vue 3 plugin cannot be installed through this Vue 2 contract.

If a new project must use Vue 3, I would change the integration boundary to one of these:

1. **Iframe:** strongest framework and security isolation; communicate with postMessage.
2. **Web component:** expose a browser custom element with properties and events.
3. **Framework-neutral mount API:** expose mount(element, props) and unmount(), and let the remote own its Vue 3 runtime inside an empty host container.
4. **Host migration:** move the host and shared integrations to Vue 3, which is the largest option.

## Artifact storage and deployment

The host and remote have independent pipelines.

The remote pipeline:

1. Installs and tests the remote project.
2. Produces the UMD JavaScript and static assets.
3. Uploads them to CDN-backed object storage.
4. Publishes or updates the selected environment version.
5. Runs a smoke or contract test against a host fixture.

The host maintains an environment-to-CDN mapping. It checks the current hostname and chooses production, QA, or a default remote URL.

For reliable storage and rollback, I would prefer immutable releases:

- Store each release under a commit or release identifier.
- Never overwrite a released asset.
- Publish an environment manifest or alias that identifies the active release.
- Roll back by moving that pointer to a previously tested version.

Content-hashed assets are another good option. Stable URLs are simpler, but CDN/browser cache invalidation and rollback become harder.

The current repository shows stable environment-specific URLs. Versioned URLs, integrity checks, and an explicit rollback pointer are good production-hardening improvements.

## Runtime loading sequence

At runtime:

1. The browser opens the Admin page.
2. The page loads the small admin_landing host bundle.
3. The host creates a Vue 2 root instance and mounts it.
4. The wrapper initially keeps the remote component hidden.
5. It identifies the current environment from the hostname.
6. It asks the generic loader for the corresponding CDN module.
7. The loader checks whether the plugin is already available or installed.
8. Otherwise, it appends a script element to the document head.
9. The browser downloads and evaluates the UMD bundle.
10. The bundle exposes **window.UiSelfServeOnboarding**.
11. The loader reads that export and installs the plugin into the host Vue constructor.
12. It passes the store, API endpoints, and i18n instance as plugin options.
13. The plugin registers **SelfServeOnboardingApp** globally.
14. The wrapper marks the remote as loaded.
15. Vue re-renders, resolves the registered component, and displays it.

The remote is loaded only on the relevant entry, so users on normal application pages do not pay its download and execution cost.

## How the global component is recognized

This is an important interview follow-up.

During plugin installation, the remote receives the host's Vue constructor and registers its root component by name. Vue 2 maintains a global component registry on that constructor.

~~~text
Shared Vue constructor
        │
        └── component registry
                └── SelfServeOnboardingApp → remote root component
~~~

The host wrapper renders the component only after installation succeeds. On that render, Vue looks up **SelfServeOnboardingApp** in the shared registry and finds the remote component.

The loaded flag prevents Vue from trying to resolve the component before registration.

Using the same Vue runtime is critical. If the remote registers against a different bundled Vue constructor, the host's registry may not know about that component.

## How state exchange works

### Shared application state

The host passes the existing Vuex store instance during plugin installation. Both sides observe the same reactive store; state is not serialized or copied.

Shared state may include:

- Current user and tenant.
- Permissions and feature flags.
- Session/configuration information.
- Data genuinely required by both the host and remote.

When the host changes shared Vuex state, subscribed remote components react. When the remote dispatches an approved shared action, host components observing that state react.

### Remote-owned state

Not all state should be shared. Form drafts, open dialogs, temporary selections, local tabs, and feature loading flags should remain in the remote.

If the remote requires Vuex modules, I would:

- Give each module a unique namespace.
- Register it once during plugin installation.
- Check whether it is already registered.
- Document whether it remains for the browser session or is removed at unmount.
- Communicate through actions and getters rather than changing unrelated host state.

This keeps the shared store from becoming an undocumented coupling point.

### API and authentication

The host passes endpoint definitions to the remote. Because the remote executes inside the authenticated host page, API requests use the existing browser session/cookie behavior and approved host configuration.

The plugin options act as dependency injection:

~~~text
Host → installation contract → Remote

store       shared reactive state
endpoints   approved backend locations
i18n        shared locale and translations
~~~

I would never pass secrets in this contract. Browser code cannot safely hold secrets.

### Contract discipline

Sharing one store is convenient but can create tight coupling. I would document a versioned public surface:

- Allowed state/getters.
- Allowed actions and payload shapes.
- Remote-owned Vuex namespace.
- Endpoint names and response expectations.
- Events or callbacks flowing back to the host.

The remote should not depend on the host's entire internal store shape.

## Routing and navigation

The current host does not provide a router in the plugin options. The remote therefore should not assume access to the main SPA router.

Possible navigation approaches are:

- Local view state for a small flow.
- Normal browser navigation for page transitions.
- A remote-owned, namespaced router with carefully managed URLs.
- Explicit navigation callbacks added to the host contract.

For a new design, I would favor explicit callbacks over letting the remote reach into an undocumented host router.

## Lifecycle and duplicate loading

The loader checks the existing browser global and Vue's installed-plugin list, preventing normal repeat installation.

For concurrent requests, I would add a promise registry:

~~~text
remote name → current loading promise
~~~

If two wrappers request the same remote simultaneously, both await the same promise instead of adding duplicate scripts.

This Admin integration is a standalone page, so page unload naturally destroys it. For a remote mounted and unmounted inside a long-running SPA, I would define cleanup for:

- Window/document event listeners.
- Timers and observers.
- Network subscriptions.
- Dynamically registered Vuex modules.
- Remote DOM and styles where applicable.

## Loading and failure handling

The module loader applies a timeout, supports ordered fallback URLs, and verifies that the expected browser global exists after script evaluation.

The UI should expose three states:

1. Loading skeleton or spinner.
2. Loaded remote application.
3. Failure UI with retry and support information.

The current Admin wrapper silently leaves the area empty if loading fails. I would describe visible failure recovery as a desired improvement, not something already implemented.

Useful telemetry includes:

- Selected environment and remote version.
- Download and installation duration.
- Script errors and timeouts.
- Missing-global or invalid-plugin errors.
- Remote rendering errors.
- Retry success rate.

A Vue error boundary/errorCaptured handler should keep a remote render error from destroying the host shell.

## Compatibility and contract testing

Independent deployment works only when the host/remote boundary is stable.

I would version and document:

- Supported Vue major/minor range.
- UMD global name.
- Plugin install shape.
- Registered root-component name.
- Plugin option types.
- Vuex namespaces/actions/getters.
- API endpoint contract.
- i18n behavior.
- Host events or callbacks.
- Minimum compatible host and remote releases.

The remote pipeline should load the built artifact into a minimal host fixture and verify:

- The expected global is created.
- It exposes a valid plugin.
- Installation succeeds against the supported Vue runtime.
- The expected component is registered.
- Required options are consumed correctly.
- The component can mount and render.

This catches integration failures before deployment. Backward compatibility also matters because cached host and remote versions can temporarily be mixed during rollout.

## Security

A runtime-loaded script executes with the same page privileges as the host. It is not isolated like an iframe.

I would therefore:

- Load scripts only from allow-listed HTTPS origins.
- Restrict Content Security Policy script sources.
- Use immutable artifacts and controlled release permissions.
- Consider Subresource Integrity for immutable URLs.
- Scan remote dependencies in its own CI pipeline.
- Minimize the state exposed to the remote.
- Never include secrets in bundles or plugin options.

If strong trust isolation were required, I would choose an iframe.

## Why UMD instead of Module Federation

The existing host already used Vue 2 and a classic Webpack setup. UMD loading provided independent deployment with limited host changes:

- It works through ordinary script loading.
- Host and remote builds remain separate.
- The remote can release without rebuilding the host.
- It works with the server-rendered Admin page.
- It does not require a Module Federation runtime migration.

The trade-off is that dependency sharing, version compatibility, lifecycle, discovery, and contract validation must be managed by our own conventions.

## Benefits and trade-offs

### Benefits

- Independent Admin release and rollback.
- Remote code is loaded only where needed.
- Clearer team ownership.
- Reuse of the authenticated host session and shared services.
- Incremental modernization without rewriting the large host.

### Trade-offs

- The plugin is coupled to Vue 2 and the integration contract.
- A shared store can create hidden coupling if not governed.
- Runtime JavaScript and CSS are not isolated.
- CDN or cache failures affect feature availability.
- Global component/style names can collide.
- Error recovery and observability require deliberate work.

## Detailed answer to give in an interview

> We had a large Vue 2 product, but we wanted the Admin experience to have an independent build and release cycle. I implemented it as a runtime-loaded UMD microfrontend.
>
> On the host side, I created a separate Webpack entry called admin_landing. It is intentionally small: it mounts a Vue 2 shell, owns the authenticated application context, and provides the existing Vuex store, API endpoint definitions, and i18n instance. It does not statically bundle the Admin feature.
>
> The Admin project has its own build pipeline. It produces a UMD library whose public global is UiSelfServeOnboarding. The library exports a Vue plugin and treats Vue as a compatible peer dependency because it installs into the host's Vue 2 runtime. We deploy that artifact to environment-specific CDN storage, independently from the host.
>
> At runtime, the wrapper determines the environment from the hostname and asks a generic loader for the appropriate CDN module. The loader appends a script tag, applies a timeout, can try fallback URLs, and verifies that the expected global appeared. It installs the plugin into the host Vue constructor and passes the store, endpoints, and i18n through a small dependency-injection contract.
>
> During installation, the remote registers its root component globally as SelfServeOnboardingApp. The wrapper keeps that component behind a loaded flag. After installation succeeds, it changes the flag; Vue re-renders, resolves the component from the shared Vue constructor's registry, and renders the remote UI.
>
> For state, both sides use one Vuex store instance only for application-level concerns such as user, tenant, permissions, and configuration. Remote-specific UI state stays local or in a uniquely namespaced module. Communication is reactive through documented actions and getters. API configuration and translations are also supplied by the host, so the remote does not duplicate authentication or hardcode environment details.
>
> The main advantage was independent delivery with minimal changes to a legacy host. The main trade-off was coupling to Vue 2 and the shared contract. We controlled that by sharing one Vue runtime, keeping the contract small, avoiding duplicate installation, namespacing feature state, and testing the built remote against a host fixture. If the remote needed Vue 3, I would change the boundary to an iframe, web component, or framework-neutral mount/unmount API.

## Fast answers for follow-up questions

### Is admin_landing itself the microfrontend?

It is more accurate to call it the **host/bootstrap entry**. The independently built and CDN-deployed UiSelfServeOnboarding bundle is the remote microfrontend.

### How can the host render something it did not compile?

The remote registers a component at runtime on the same Vue constructor. On the next render, Vue resolves it from the global component registry.

### How is state shared?

The host passes the existing Vuex store during plugin installation. Shared application state uses documented, namespaced Vuex APIs; feature-only state remains private.

### How is authentication shared?

The remote executes in the authenticated host page and uses the established browser session plus host-provided endpoint configuration. Secrets are never sent through the frontend contract.

### Can the remote use Vue 3?

Not with this Vue 2 plugin/global-component boundary. Vue 3 requires isolation through an iframe, web component, or framework-neutral mount API.

### How is it deployed independently?

The remote pipeline uploads the UMD artifact to CDN-backed storage. The host selects an environment URL at runtime. Immutable versioned assets plus an environment manifest provide safe rollout and rollback.

### What happens if the CDN is unavailable?

The loader times out and can try fallback URLs. The intended UI behavior is a visible error state with retry while the host stays usable. Silent failure in the current wrapper is an improvement opportunity.

### How do you prevent duplicate loading?

The loader checks the browser global and the Vue installed-plugin list. A shared in-flight promise registry prevents duplicate simultaneous downloads.

### Why not publish an npm package?

An npm package is linked at build time, so each Admin release would require rebuilding and deploying the host. Runtime CDN loading enables independent deployment.

### Why not use an iframe?

The plugin approach gives tighter integration with Vuex, i18n, the session, and the existing visual experience. An iframe gives stronger isolation and would be preferable for framework independence or a lower-trust remote.

### Why not use Module Federation?

UMD fit the existing Vue 2/Webpack architecture with less migration. Module Federation could add dependency-sharing and remote-discovery tooling, but was not required for this integration.

## Claims to avoid

Do not say:

- admin_landing is Vue 3; it is Vue 2.
- This uses Module Federation; it uses runtime UMD loading.
- The runtime plugin is isolated like an iframe; it executes in the host page.
- All state belongs in the shared store; remote-only state should stay private.
- The current wrapper already shows a retry screen; its current failure handling is silent.
- The backend template or the remote project's exact build configuration is present here; those are outside this repository.
