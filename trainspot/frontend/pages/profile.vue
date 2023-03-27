<template>
  <div v-if="user">
    <user-info :user="user" :subscription="subscription" />
  </div>
</template>

<script>
  import UserInfo from '@/components/UserInfo.vue'
  import {mapGetters} from "vuex";
  export default {
    name: "profile",
    modules: [UserInfo],
    mounted() {
      this.$store.dispatch("user/fetchUser")
      this.$store.dispatch("user/fetchSubscription", {userId: this.$store.state.user.data.id})
    },
    user() {
      return this.$store.state.user.data
    },
    subscription() {
      return this.$store.state.user.subscription
    },
    computed: {
      ...mapGetters({
        user: "user/getUser",
        subscription: "user/getSubscription"
      })
    },

  }
</script>
