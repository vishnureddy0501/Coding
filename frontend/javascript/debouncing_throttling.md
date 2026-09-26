debounce:
--------
clearTimeout(timer) → cancels the alarm
timer = null        → it simply sets timer variable to null. we just lost the reference to settimeout with this.

At the beginning
-------------------
    clearTimeout(this.timer);
    Cancels the previous pending callback when the user types again.

Inside the callback
--------------------
this.timer = null;
Indicates that no timer is currently pending because the callback has finished.

clearTimeout(this.timer); // Cancels Timeout #1
this.timer = setTimeout(...); // Creates Timeout #2

| Statement | Cancels the callback? | Changes your variable? |
|---|---:|---:|
| `clearTimeout(this.timer)` | Yes | No |
| `this.timer = null` | No | Yes |

for cleanup:
------------
beforeDestroy() {
  clearTimeout(this.timer);
  this.timer = null;
}


<template>
    <div>
      <input type="text" v-model="search" />
    </div>
</template>
<script>
  export default {
    data () {
      return {
        search: '',
        timer: null
      }
    },
    watch: {
      search (val) {
        this.debouncedSearch(val);
      }
    },
      beforeDestroy() {
        // cleanup the watcher if any.
        clearTimeout(this.timer);
    },
    methods: {
      debouncedSearch (val) {
        clearTimeout(this.timer);
        this.timer = setTimeout(() => {
          console.log("api called", val);
        }, 1000);
      }
    }
  }
</script>


throttling:
-----------
/*
When the user types the first character:
- timer is null, so a timer starts.
- Additional inputs during the next second are ignored.
- After one second, the API uses the first value captured when the timer started.
- The timer is reset, allowing another call.

*/
<template>
  <div>
    <input
      v-model="search"
      type="text"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      timer: null
    };
  },

  watch: {
    search(value) {
      this.throttledSearch(value);
    }
  },

  beforeDestroy() {
    clearTimeout(this.timer);
  },

  methods: {
    throttledSearch() {
      if (this.timer) {
        return;
      }

      this.timer = setTimeout(() => {
        console.log("API called:", this.search);

        this.timer = null;
      }, 1000);
    }
  }
};
</script>