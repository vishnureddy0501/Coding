<template>
  <div>
    <LabHeader
      number="05"
      title="API versus UI timeline"
      description="Simulate a fast response followed by expensive client processing so you can locate the real delay."
      task="Record Chrome Performance and Vue Timeline, click Load data, then find the delay between API completion and DOM update."
    />

    <section class="panel controls">
      <label class="field">
        <span>Simulated API delay</span>
        <select v-model.number="apiDelay"><option :value="300">300 ms</option><option :value="1000">1 second</option></select>
      </label>
      <label class="checkbox"><input v-model="slowProcessing" type="checkbox"> Add expensive UI processing</label>
      <button :disabled="loading" @click="loadData">{{ loading ? 'Loading…' : 'Load data' }}</button>
    </section>

    <div class="metrics-grid">
      <div class="metric-card"><span>API</span><strong>{{ timings.api }} ms</strong></div>
      <div class="metric-card"><span>Processing</span><strong>{{ timings.processing }} ms</strong></div>
      <div class="metric-card"><span>Total until state update</span><strong>{{ timings.total }} ms</strong></div>
    </div>

    <section class="panel">
      <div class="section-title"><h3>Result preview</h3><span>{{ rows.length }} rows</span></div>
      <div class="table-wrap">
        <table><thead><tr><th>Name</th><th>Score</th><th>Segment</th></tr></thead>
          <tbody><tr v-for="row in rows.slice(0, 30)" :key="row.id"><td>{{ row.name }}</td><td>{{ row.score }}</td><td>{{ row.segment }}</td></tr></tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script>
import LabHeader from '../components/LabHeader.vue';

const wait = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));
const makeRows = (count) => Array.from({ length: count }, (_, index) => ({
  id: index + 1, name: `Account ${String(index + 1).padStart(4, '0')}`,
  score: (index * 37) % 101, segment: ['Growth', 'Enterprise', 'SMB'][index % 3]
}));

export default {
  name: 'NetworkLab',
  components: { LabHeader },
  data() {
    return { apiDelay: 1000, slowProcessing: true, loading: false, rows: [], timings: { api: 0, processing: 0, total: 0 } };
  },
  methods: {
    async loadData() {
      this.loading = true;
      const totalStart = performance.now();
      const apiStart = performance.now();
      await wait(this.apiDelay);
      const response = makeRows(2500);
      this.timings.api = Math.round(performance.now() - apiStart);

      const processingStart = performance.now();
      let rows = response;
      if (this.slowProcessing) {
        // Deliberately waste CPU by repeatedly sorting copies. Find this long task in Chrome Performance.
        for (let index = 0; index < 180; index += 1) {
          rows = [...rows].sort((a, b) => index % 2 ? a.name.localeCompare(b.name) : b.score - a.score);
        }
      } else {
        rows = [...rows].sort((a, b) => b.score - a.score);
      }
      this.timings.processing = Math.round(performance.now() - processingStart);
      this.rows = rows;
      this.timings.total = Math.round(performance.now() - totalStart);
      this.loading = false;
    }
  }
};
</script>
