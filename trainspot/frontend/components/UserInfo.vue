<template>
  <div>
    <v-layout flex align-center justify-center>
      <v-flex xs8 sm8 elevation-8>
        <v-card>
          <v-card-title flex align-center justify-center>
            <h1>Информация о пользователе</h1>
          </v-card-title>
          <v-card-text class="pt-4">
            <p>username: {{ user.username }}</p>
            <p>Email: {{ user.email }}</p>
            <p>Role: {{ user.role }}</p>
          </v-card-text>
        </v-card>
        <v-card>
          <div class="d-flex align-center justify-space-between">
            <v-card-title>
              <h1>Абонемент</h1>
            </v-card-title>
            <buy-plan/>
          </div>
          <v-card-text class="pt-4" v-if="subscription">
            <p>Куплен: {{ subscription.start_date }}</p>
            <p>Осталось посещений: {{ subscription.visits_left }}</p>
            <p>Осталось дней: {{subscription.days_left}}</p>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import BuyPlan from "@/components/BuyPlan.vue";
export default {
  name: "UserInfo",
  components: {
    BuyPlan
  },
  props: {
    user: {
      type: Object,
      required: true
    },
  },
  computed: {
    subscription() {
      return this.$store.state.user.subscription;
    },
  },
  created() {
    this.$store.dispatch("user/fetchSubscription", {userId: this.user.id})
  },
}
</script>
