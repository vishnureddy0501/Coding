<template>
  <label class="field">
    <span>Search users</span>
    <input :value="value" placeholder="Type a name or role" @input="$emit('input', $event.target.value)" />
  </label>
</template>

<script>
export default {
  name: 'SearchBox',
  props: { value: { type: String, default: '' } }
};
</script>
