<template>
  <div>
    <LabHeader
      number="00"
      title="Start here"
      description="A guided playground for inspecting Vue 2 applications instead of learning DevTools on an unpredictable production screen."
      task="Open Vue DevTools, select the Components tab, and find App → HomeLab → LabHeader."
    />

    <section class="panel">
      <h3>Recommended setup</h3>
      <ol class="steps">
        <li>Install the Vue.js DevTools browser extension and allow it on localhost.</li>
        <li>Open browser DevTools and locate the Vue tab.</li>
        <li>Keep the Console, Network, Performance, and Vue tabs available.</li>
        <li>Work through the sections in order, then solve the debugging challenges.</li>
      </ol>
    </section>

    <div class="card-grid">
      <article v-for="topic in topics" :key="topic.title" class="topic-card">
        <span>{{ topic.number }}</span>
        <h3>{{ topic.title }}</h3>
        <p>{{ topic.description }}</p>
      </article>
    </div>

    <section class="callout">
      <strong>Important:</strong> deliberately inefficient code is labelled in the UI and source. Use it to observe symptoms, then enable the optimized version and compare recordings.
    </section>
  </div>
</template>

<script>
import LabHeader from '../components/LabHeader.vue';

export default {
  name: 'HomeLab',
  components: { LabHeader },
  data() {
    return {
      topics: [
        { number: '01', title: 'Component tree', description: 'Inspect local state, props, computed values, and nested components.' },
        { number: '02', title: 'Events', description: 'Trace custom events and parent-child data flow.' },
        { number: '03', title: 'Reactivity', description: 'Compare computed caching, methods, and watchers.' },
        { number: '04', title: 'Vuex', description: 'Observe actions, mutations, getters, and state history.' },
        { number: '05', title: 'Timing', description: 'Separate API latency from processing and rendering.' },
        { number: '06', title: 'Rendering', description: 'Profile large lists and unnecessary updates.' },
        { number: '07', title: 'Lifecycle', description: 'See mount, update, and destroy behavior.' },
        { number: '08', title: 'Debugging', description: 'Find realistic bugs using evidence.' }
      ]
    };
  }
};
</script>
