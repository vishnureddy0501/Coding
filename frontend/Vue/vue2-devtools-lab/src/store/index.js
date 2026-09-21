import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const wait = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

export default new Vuex.Store({
  strict: process.env.NODE_ENV !== 'production',
  state: {
    user: { id: 1, name: 'Vishnu', role: 'Engineer' },
    notifications: [],
    unreadCount: 0,
    activity: []
  },
  getters: {
    unreadNotifications: (state) => state.notifications.filter((item) => !item.read),
    notificationSummary: (state) => `${state.unreadCount} unread of ${state.notifications.length}`
  },
  mutations: {
    ADD_NOTIFICATION(state, notification) {
      state.notifications.unshift(notification);
      state.unreadCount += 1;
    },
    MARK_ALL_READ(state) {
      state.notifications = state.notifications.map((item) => ({ ...item, read: true }));
      state.unreadCount = 0;
    },
    ADD_ACTIVITY(state, message) {
      state.activity.unshift({ id: Date.now() + Math.random(), message, time: new Date().toLocaleTimeString() });
    },
    CLEAR_ACTIVITY(state) {
      state.activity = [];
    }
  },
  actions: {
    async createNotification({ commit }, text) {
      commit('ADD_ACTIVITY', 'Action started');
      await wait(500);
      commit('ADD_NOTIFICATION', { id: Date.now(), text, read: false });
      commit('ADD_ACTIVITY', 'Notification committed after 500 ms');
    },
    markAllRead({ commit }) {
      commit('MARK_ALL_READ');
      commit('ADD_ACTIVITY', 'All notifications marked as read');
    }
  }
});
