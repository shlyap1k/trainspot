<template>
  <div>
    <user-info :user="user" :subscription="subscription" />
  </div>
</template>

<script>
  import UserInfo from '@/components/UserInfo.vue'
  export default {
    name: "profile",
    modules: [UserInfo],
    computed: {
      user() {
        return this.$store.state.user.data
      },
      subscription() {
        return this.$store.state.user.subscription
      }
    },
    mounted() {
      this.$store.dispatch("user/fetchUser")
      this.$store.dispatch("user/fetchSubscription")
    }
  }
</script>
