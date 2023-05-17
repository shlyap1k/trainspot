<template>
  <div v-if="user">
    <user-info :user="user"/>
    <appeal-form :user="user"/>
  </div>
</template>

<script>
  import UserInfo from '@/components/UserInfo.vue'
  import {mapGetters} from "vuex";
  import AppealForm from "@/components/Forms/AppealForm.vue";
  export default {
    name: "profile",
    components: {
      UserInfo,
      AppealForm
    },
    mounted() {
      this.$store.dispatch("user/fetchUser")
    },
    methods: {
      get_subscription() {
        this.$store.dispatch("user/fetchSubscription", {userId: this.$store.state.user.data.id})
      }
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
