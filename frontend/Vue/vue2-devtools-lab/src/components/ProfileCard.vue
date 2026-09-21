<template>
  <article class="profile-card" :class="{ selected: isSelected }">
    <button class="avatar" @click="$emit('select', user.id)">{{ initials }}</button>
    <div>
      <h3>{{ user.name }}</h3>
      <p>{{ user.role }} · {{ user.team }}</p>
      <small>Local clicks: {{ localClicks }}</small>
    </div>
    <button class="secondary" @click="handleInspect">Inspect</button>
  </article>
</template>

<script>
export default {
  name: 'ProfileCard',
  props: {
    user: { type: Object, required: true },
    isSelected: { type: Boolean, default: false }
  },
  data() {
    return { localClicks: 0 };
  },
  computed: {
    initials() {
      return this.user.name.split(' ').map((part) => part[0]).join('').slice(0, 2);
    }
  },
  methods: {
    handleInspect() {
      this.localClicks += 1;
      this.$emit('inspect', { ...this.user, inspectedAt: new Date().toLocaleTimeString() });
    }
  }
};
</script>
