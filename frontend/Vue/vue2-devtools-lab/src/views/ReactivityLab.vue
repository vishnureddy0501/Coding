<template>
  <div>
    <LabHeader
      number="03"
      title="Computed properties and watchers"
      description="Compare cached computed values with template methods and observe a watcher that causes side effects."
      task="Type in the search box, inspect computed values, and compare the computed-run and method-run counters."
    />

    <section class="panel controls">
      <label class="field grow">
        <span>Search products</span>
        <input v-model="search" placeholder="Try 'pro'" />
      </label>
      <button class="secondary" @click="unrelatedCounter += 1">Unrelated update: {{ unrelatedCounter }}</button>
    </section>

    <div class="metrics-grid">
      <div class="metric-card"><span>Computed executions</span><strong>{{ _computedRuns }}</strong></div>
      <div class="metric-card"><span>Method executions</span><strong>{{ _methodRuns }}</strong></div>
      <div class="metric-card"><span>Watcher executions</span><strong>{{ watcherRuns }}</strong></div>
    </div>

    <section class="two-column">
      <article class="panel">
        <h3>Computed result</h3>
        <p v-for="product in filteredWithComputed" :key="product.id">{{ product.name }}</p>
      </article>
      <article class="panel">
        <h3>Method result</h3>
        <p v-for="product in filteredWithMethod()" :key="product.id">{{ product.name }}</p>
        <small>The method runs again whenever this component renders.</small>
      </article>
    </section>

    <section class="panel">
      <h3>Debounced watcher result</h3>
      <p>{{ watcherMessage }}</p>
      <p class="muted">The watcher waits 400 ms after typing stops. Watch its state and component updates in DevTools.</p>
    </section>
  </div>
</template>

<script>
import LabHeader from '../components/LabHeader.vue';

export default {
  name: 'ReactivityLab',
  components: { LabHeader },
  beforeCreate() {
    // Underscore-prefixed fields are intentionally non-reactive so counting a render does not trigger another render.
    this._computedRuns = 0;
    this._methodRuns = 0;
  },
  data() {
    return {
      search: '', unrelatedCounter: 0, watcherRuns: 0,
      watcherMessage: 'Waiting for input', watcherTimer: null,
      products: [
        { id: 1, name: 'Analytics Pro' }, { id: 2, name: 'Sales Workspace' },
        { id: 3, name: 'Forecast Studio' }, { id: 4, name: 'Prospect Manager' }
      ]
    };
  },
  computed: {
    filteredWithComputed() {
      // The counter is for learning visibility; side effects inside computed properties are not recommended.
      this._computedRuns += 1;
      const query = this.search.toLowerCase();
      return this.products.filter((product) => product.name.toLowerCase().includes(query));
    }
  },
  watch: {
    search(value) {
      this.watcherRuns += 1;
      clearTimeout(this.watcherTimer);
      this.watcherMessage = 'Waiting for typing to stop…';
      this.watcherTimer = setTimeout(() => {
        this.watcherMessage = `A request would run for “${value}”`;
      }, 400);
    }
  },
  beforeDestroy() {
    clearTimeout(this.watcherTimer);
  },
  methods: {
    filteredWithMethod() {
      this._methodRuns += 1;
      const query = this.search.toLowerCase();
      return this.products.filter((product) => product.name.toLowerCase().includes(query));
    }
  }
};
</script>
