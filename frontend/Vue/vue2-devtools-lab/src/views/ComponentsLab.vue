<template>
  <div>
    <LabHeader
      number="01"
      title="Component inspector"
      description="Explore a nested component tree and follow data from parent state into child props and computed values."
      task="Select a ProfileCard, edit its user prop or localClicks value, and watch the screen change immediately."
    />

    <section class="panel controls">
      <SearchBox v-model="query" />
      <label class="field">
        <span>Team</span>
        <select v-model="teamFilter">
          <option value="all">All teams</option>
          <option>Platform</option>
          <option>Product</option>
        </select>
      </label>
      <p class="metric">Visible: <strong>{{ filteredUsers.length }}</strong></p>
    </section>

    <div class="stack">
      <ProfileCard
        v-for="user in filteredUsers"
        :key="user.id"
        :user="user"
        :is-selected="selectedId === user.id"
        @select="selectedId = $event"
        @inspect="lastInspected = $event"
      />
    </div>

    <section class="panel" v-if="lastInspected">
      <h3>Last emitted payload</h3>
      <pre>{{ lastInspected }}</pre>
    </section>
  </div>
</template>

<script>
import LabHeader from '../components/LabHeader.vue';
import ProfileCard from '../components/ProfileCard.vue';
import SearchBox from '../components/SearchBox.vue';

export default {
  name: 'ComponentsLab',
  components: { LabHeader, ProfileCard, SearchBox },
  data() {
    return {
      query: '',
      teamFilter: 'all',
      selectedId: null,
      lastInspected: null,
      users: [
        { id: 1, name: 'Asha Rao', role: 'Frontend Engineer', team: 'Product' },
        { id: 2, name: 'Ravi Kumar', role: 'API Engineer', team: 'Platform' },
        { id: 3, name: 'Meera Shah', role: 'Product Designer', team: 'Product' },
        { id: 4, name: 'Arjun Nair', role: 'Site Reliability Engineer', team: 'Platform' }
      ]
    };
  },
  computed: {
    filteredUsers() {
      const query = this.query.toLowerCase();
      return this.users.filter((user) => {
        const matchesQuery = `${user.name} ${user.role}`.toLowerCase().includes(query);
        const matchesTeam = this.teamFilter === 'all' || user.team === this.teamFilter;
        return matchesQuery && matchesTeam;
      });
    }
  }
};
</script>
