<template>
  <div>
    <LabHeader
      number="06"
      title="Rendering performance"
      description="Compare rendering every row with a small visible window and observe how unrelated state affects the component."
      task="Record a Performance trace in full-list mode, change the highlight color, then switch to optimized mode and compare scripting/rendering time and DOM size."
    />

    <section class="panel controls">
      <label class="field"><span>Rows</span><select v-model.number="rowCount"><option :value="500">500</option><option :value="2000">2,000</option><option :value="5000">5,000</option></select></label>
      <label class="checkbox"><input v-model="optimized" type="checkbox"> Optimized window (60 rows)</label>
      <label class="field"><span>Highlight</span><input v-model="highlight" type="color"></label>
      <button class="secondary" @click="unrelated += 1">Unrelated update {{ unrelated }}</button>
    </section>

    <div class="metrics-grid">
      <div class="metric-card"><span>Generated rows</span><strong>{{ rows.length }}</strong></div>
      <div class="metric-card"><span>DOM rows</span><strong>{{ visibleRows.length }}</strong></div>
      <div class="metric-card"><span>Previous updates</span><strong>{{ _updateCount }}</strong></div>
    </div>

    <section class="panel dense-list">
      <div v-for="row in visibleRows" :key="row.id" class="data-row">
        <span class="color-block" :style="{ background: highlight }"></span>
        <strong>{{ row.name }}</strong><span>{{ row.email }}</span><span>{{ row.score }}</span>
      </div>
    </section>
  </div>
</template>

<script>
import LabHeader from '../components/LabHeader.vue';

export default {
  name: 'PerformanceLab',
  components: { LabHeader },
  beforeCreate() { this._updateCount = 0; },
  data() { return { rowCount: 2000, optimized: false, highlight: '#6d5dfc', unrelated: 0 }; },
  computed: {
    rows() {
      return Array.from({ length: this.rowCount }, (_, index) => ({
        id: index, name: `Customer ${index + 1}`, email: `customer${index + 1}@example.com`, score: (index * 29) % 100
      }));
    },
    visibleRows() { return this.optimized ? this.rows.slice(0, 60) : this.rows; }
  },
  // Non-reactive on purpose: changing reactive state from updated() would create an update loop.
  updated() { this._updateCount += 1; }
};
</script>
