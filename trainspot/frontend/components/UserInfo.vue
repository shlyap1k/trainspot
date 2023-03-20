<template>
  <div>
    <v-layout flex align-center justify-center>
      <v-flex xs6 sm6 elevation-6>
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
          <v-card-title flex align-center justify-center>
            <h1>Абонемент</h1>
          </v-card-title>
          <v-card-text class="pt-4">
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
export default {
  name: "UserInfo",
  props: {
    user: {
      type: Object,
      required: true
    },
    subscription: {
      type: Object,
      required: true
    }
  }
}
</script>
