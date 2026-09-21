<template>
  <section class="panel lifecycle-child">
    <h3>Mounted child #{{ instanceId }}</h3>
    <p>Counter: {{ counter }}</p>
    <button @click="counter += 1">Trigger update</button>
  </section>
</template>

<script>
export default {
  name: 'LifecycleChild',
  data() {
    return { counter: 0, instanceId: Math.floor(Math.random() * 10000), timer: null };
  },
  beforeCreate() { this.report('beforeCreate'); },
  created() { this.report('created'); },
  beforeMount() { this.report('beforeMount'); },
  mounted() {
    this.report('mounted');
    this.timer = setInterval(() => this.$emit('heartbeat', new Date().toLocaleTimeString()), 3000);
  },
  beforeUpdate() { this.report('beforeUpdate'); },
  updated() { this.report('updated'); },
  beforeDestroy() {
    this.report('beforeDestroy');
    clearInterval(this.timer);
  },
  destroyed() { this.report('destroyed'); },
  methods: {
    report(hook) {
      this.$emit('hook-fired', { hook, at: new Date().toLocaleTimeString() });
    }
  }
};
</script>
