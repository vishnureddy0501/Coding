<template>
  <div>
    <LabHeader
      number="08"
      title="Debugging challenges"
      description="Use the component inspector, Vuex history, Network panel, and timeline to diagnose symptoms before revealing the explanation."
      task="Solve each challenge using tools first. Reveal the answer only after writing down your evidence."
    />

    <section v-for="challenge in challenges" :key="challenge.id" class="panel challenge">
      <div class="section-title"><div><span class="badge">Challenge {{ challenge.id }}</span><h3>{{ challenge.title }}</h3></div></div>
      <p><strong>Symptom:</strong> {{ challenge.symptom }}</p>
      <p><strong>What to inspect:</strong> {{ challenge.inspect }}</p>
      <button class="secondary" @click="toggle(challenge.id)">{{ revealed.includes(challenge.id) ? 'Hide answer' : 'Reveal answer' }}</button>
      <div v-if="revealed.includes(challenge.id)" class="answer"><strong>Likely cause and fix:</strong> {{ challenge.answer }}</div>
    </section>
  </div>
</template>

<script>
import LabHeader from '../components/LabHeader.vue';

export default {
  name: 'DebuggingLab',
  components: { LabHeader },
  data() {
    return {
      revealed: [],
      challenges: [
        { id: 1, title: 'API is fast, screen is slow', symptom: 'The response arrives in one second, but content appears much later.', inspect: 'Network request start/end, main-thread long tasks, Vue component updates, response size.', answer: 'The Network lab adds repeated sorting after the response. Move or reduce transformation work, use a lookup-efficient algorithm, paginate, or process outside the critical render path.' },
        { id: 2, title: 'Too many renders', symptom: 'Changing an unrelated button makes a large screen expensive.', inspect: 'Vue Timeline component updates and Chrome Performance rendering/layout.', answer: 'The Performance lab renders thousands of DOM nodes. Render only the visible window, paginate, and keep frequently changing state away from large subtrees.' },
        { id: 3, title: 'Duplicate behavior', symptom: 'One interaction appears to create several state changes.', inspect: 'Vue custom events plus Vuex action and mutation history.', answer: 'Establish whether multiple events were deliberately emitted, multiple listeners exist, or both a watcher and click handler invoke the same action. Keep one owner for each side effect.' },
        { id: 4, title: 'Component keeps working after removal', symptom: 'Logs or requests continue after navigating away.', inspect: 'Component tree, lifecycle log, timers, subscriptions, and event listeners.', answer: 'A timer or listener was not cleaned up. Store its reference and remove it in beforeDestroy. The Lifecycle lab demonstrates correct cleanup.' },
        { id: 5, title: 'Displayed data is incorrect', symptom: 'A child shows unexpected user information.', inspect: 'Walk from the child prop to parent computed data and original state in Components.', answer: 'Find the first layer where data becomes incorrect: API/store, parent state, computed filtering, prop, or child transformation. Fix that layer instead of patching the rendered text.' }
      ]
    };
  },
  methods: {
    toggle(id) {
      this.revealed = this.revealed.includes(id) ? this.revealed.filter((item) => item !== id) : [...this.revealed, id];
    }
  }
};
</script>
