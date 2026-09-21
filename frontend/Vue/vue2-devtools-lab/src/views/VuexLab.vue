<template>
  <div>
    <LabHeader
      number="04"
      title="Vuex state inspection"
      description="Observe the complete action → mutation → state → getter → UI flow."
      task="Open the Vuex tab, dispatch an async notification, inspect its two mutations, then use state time travel if your DevTools version supports it."
    />

    <section class="panel">
      <div class="section-title">
        <div><h3>{{ user.name }}</h3><p>{{ user.role }}</p></div>
        <span class="badge">{{ notificationSummary }}</span>
      </div>
      <label class="field">
        <span>Notification text</span>
        <input v-model="notificationText" />
      </label>
      <div class="button-row">
        <button @click="addNotification">Dispatch async action</button>
        <button class="secondary" @click="markAllRead">Mark all read</button>
        <button class="secondary" @click="$store.commit('CLEAR_ACTIVITY')">Clear activity</button>
      </div>
    </section>

    <section class="two-column">
      <article class="panel">
        <h3>Unread getter</h3>
        <p v-if="!unreadNotifications.length" class="muted">No unread notifications</p>
        <ul class="plain-list"><li v-for="item in unreadNotifications" :key="item.id">{{ item.text }}</li></ul>
      </article>
      <article class="panel">
        <h3>Mutation activity</h3>
        <ul class="log-list"><li v-for="item in activity" :key="item.id"><span>{{ item.time }}</span>{{ item.message }}</li></ul>
      </article>
    </section>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex';
import LabHeader from '../components/LabHeader.vue';

export default {
  name: 'VuexLab',
  components: { LabHeader },
  data() { return { notificationText: 'New account needs attention' }; },
  computed: {
    ...mapState(['user', 'activity']),
    ...mapGetters(['unreadNotifications', 'notificationSummary'])
  },
  methods: {
    ...mapActions(['createNotification', 'markAllRead']),
    addNotification() {
      const text = this.notificationText.trim();
      if (text) this.createNotification(text);
    }
  }
};
</script>
