<template>
  <div>
    <LabHeader
      number="07"
      title="Lifecycle and cleanup"
      description="Mount, update, and destroy a component while observing hooks and a timer that must be cleaned up."
      task="Enable the child, trigger an update, wait for a heartbeat, then destroy it and verify that heartbeats stop."
    />

    <section class="panel controls">
      <button @click="showChild = !showChild">{{ showChild ? 'Destroy child' : 'Mount child' }}</button>
      <button class="secondary" @click="logs = []">Clear log</button>
    </section>

    <LifecycleChild v-if="showChild" @hook-fired="recordHook" @heartbeat="recordHeartbeat" />

    <section class="panel">
      <h3>Lifecycle log</h3>
      <ul class="log-list"><li v-for="entry in logs" :key="entry.id"><span>{{ entry.time }}</span>{{ entry.message }}</li></ul>
    </section>
  </div>
</template>

<script>
import LabHeader from '../components/LabHeader.vue';
import LifecycleChild from '../components/LifecycleChild.vue';

export default {
  name: 'LifecycleLab',
  components: { LabHeader, LifecycleChild },
  data() { return { showChild: false, logs: [] }; },
  methods: {
    add(message, time = new Date().toLocaleTimeString()) { this.logs.unshift({ id: Date.now() + Math.random(), message, time }); },
    recordHook(event) { this.add(`Hook: ${event.hook}`, event.at); },
    recordHeartbeat(time) { this.add('Timer heartbeat', time); }
  }
};
</script>
