<template>
  <section class="lab-header">
    <p class="eyebrow">{{ number }}</p>
    <h2>{{ title }}</h2>
    <p>{{ description }}</p>
    <div class="devtools-task"><strong>DevTools task:</strong> {{ task }}</div>
  </section>
</template>

<script>
export default {
  name: 'LabHeader',
  props: {
    number: { type: String, required: true },
    title: { type: String, required: true },
    description: { type: String, required: true },
    task: { type: String, required: true }
  }
};
</script>
