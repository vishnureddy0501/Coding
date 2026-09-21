<template>
  <section class="panel">
    <h3>Child component</h3>
    <p>Prop from parent: <strong>{{ message }}</strong></p>
    <label class="field">
      <span>Payload</span>
      <input v-model="payload" />
    </label>
    <div class="button-row">
      <button @click="$emit('send-message', payload)">Emit once</button>
      <button class="warning" @click="emitBurst">Emit 3-event burst</button>
    </div>
  </section>
</template>

<script>
export default {
  name: 'EventChild',
  props: { message: { type: String, required: true } },
  data() {
    return { payload: 'Hello from child' };
  },
  methods: {
    emitBurst() {
      ['started', 'processing', 'complete'].forEach((status) => this.$emit('status-change', status));
    }
  }
};
</script>
