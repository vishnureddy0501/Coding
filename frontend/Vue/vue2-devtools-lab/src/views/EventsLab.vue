<template>
  <div>
    <LabHeader
      number="02"
      title="Props and custom events"
      description="See one-way prop flow, v-model behavior, emitted payloads, and event bursts."
      task="Record the Vue Timeline, emit a three-event burst, and inspect each status-change event and component update."
    />

    <section class="panel">
      <h3>Parent component</h3>
      <label class="field">
        <span>Message passed as a prop</span>
        <input v-model="parentMessage" />
      </label>
      <p>Last child message: <strong>{{ childMessage || 'Nothing emitted yet' }}</strong></p>
      <p>Status: <span class="badge">{{ status }}</span></p>
    </section>

    <EventChild
      :message="parentMessage"
      @send-message="receiveMessage"
      @status-change="receiveStatus"
    />

    <section class="panel">
      <div class="section-title">
        <h3>Event log</h3>
        <button class="secondary" @click="eventLog = []">Clear</button>
      </div>
      <ul class="log-list">
        <li v-for="entry in eventLog" :key="entry.id"><span>{{ entry.time }}</span>{{ entry.text }}</li>
      </ul>
    </section>
  </div>
</template>

<script>
import LabHeader from '../components/LabHeader.vue';
import EventChild from '../components/EventChild.vue';

export default {
  name: 'EventsLab',
  components: { LabHeader, EventChild },
  data() {
    return { parentMessage: 'Data belongs to the parent', childMessage: '', status: 'idle', eventLog: [] };
  },
  methods: {
    log(text) {
      this.eventLog.unshift({ id: Date.now() + Math.random(), time: new Date().toLocaleTimeString(), text });
    },
    receiveMessage(message) {
      this.childMessage = message;
      this.log(`send-message: ${message}`);
    },
    receiveStatus(status) {
      this.status = status;
      this.log(`status-change: ${status}`);
    }
  }
};
</script>
