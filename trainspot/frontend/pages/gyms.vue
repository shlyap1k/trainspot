<template>
  <div>
    <h1>Gyms List</h1>
    <ul>
      <li v-for="gym in gyms" :key="gym.id">{{ gym.name }}</li>
    </ul>
    <ul>
      <li v-for="sub in subs" :key="subs.id">{{ sub.start_date }} | {{sub.visits_left}}</li>
    </ul>
  </div>
</template>

<script>
  import apiClient from '~/src/apiClient'

  export default {
    name: "",
    data() {
      return {
        // gyms: [],
        subs: []
      }
    },
    computed: {
      user: function (){
        return this.$store.state.user.data
      },
      gyms() {
        return this.$store.state.gyms.gyms
      }
    },
    mounted() {
      this.$store.dispatch("gyms/fetchGyms")
      this.$store.dispatch("user/fetchUser")
      console.log("TEST")
      console.log(this.$store.state.gyms.gyms)
    }
  }
</script>
