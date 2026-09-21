<template>
  <div id="app">
    <header class="topbar">
      <div>
        <p class="eyebrow">Vue 2 · JavaScript</p>
        <h1>DevTools Learning Lab</h1>
      </div>
      <div class="header-status">
        <span class="status-dot"></span>
        Development mode
      </div>
    </header>

    <div class="layout">
      <nav class="sidebar" aria-label="Lab sections">
        <router-link v-for="item in navigation" :key="item.path" :to="item.path">
          <span class="nav-number">{{ item.number }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>

      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      navigation: [
        { number: '00', label: 'Start here', path: '/' },
        { number: '01', label: 'Components', path: '/components' },
        { number: '02', label: 'Props & events', path: '/events' },
        { number: '03', label: 'Computed & watchers', path: '/reactivity' },
        { number: '04', label: 'Vuex', path: '/vuex' },
        { number: '05', label: 'API timeline', path: '/network' },
        { number: '06', label: 'Rendering', path: '/performance' },
        { number: '07', label: 'Lifecycle', path: '/lifecycle' },
        { number: '08', label: 'Debug challenges', path: '/debugging' }
      ]
    };
  }
};
</script>
