<template>
  <v-dialog v-model="dialog" max-width="400px">
    <v-card>
      <v-card-title class="headline">
        {{ plan.name }}
      </v-card-title>
      <v-card-text>
        <p>{{ plan.description }}</p>
        <p>Цена: {{ plan.price }} руб.</p>
        <p>Количество посещений: {{ plan.visits_count }}</p>
        <p>Продолжительность: {{ plan.duration_days }} дней</p>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="buyPlan">Купить</v-btn>
        <v-btn color="secondary" @click="closeDialog">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";
import apiClient from "@/src/apiClient";

export default {
  name: "BuyPlanForm",
  props: {
    plan: Object,
    dialog: Boolean,
  },
  data() {
    return {
      dialog: false
    }
  },
  methods: {
    buyPlan() {
      // TODO: send API request to buy the plan
      try {
        if (this.$store.state.user.subscription) {
          this.$toast.info(`У вас уже есть действующий абонемент`);
        } else {
          const data = new FormData();
          data.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
          data.append('visits_left', this.plan.visits_count)
          data.append('user', this.$store.state.user.data.id)
          data.append('plan', this.plan.id)
          axios({
              method: 'post',
              url: 'http://localhost:8000/api/subscriptions/',
              data: data,
              withCredentials: true,
              header: {
                'Accept': 'application/json',
                'Content-Type': 'multipart/form-data',
              },
          })
          const data2 = new FormData();
          data2.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
          data2.append('amount', this.plan.price)
          data2.append('description', 'Покупка абонемента')
          data2.append('type', 1)
          data2.append('user', this.$store.state.user.data.id)
          data2.append('plan', this.plan.id)
          axios({
              method: 'post',
              url: 'http://localhost:8000/api/financialrecords/',
              data: data2,
              withCredentials: true,
              header: {
                'Accept': 'application/json',
                'Content-Type': 'multipart/form-data',
              },
          })

          this.$store.dispatch('user/fetchSubscription', {userId: this.$store.state.user.data.id})
          this.$toast.success(`Абонемент куплен`);
        }
      } catch (error) {
        // Выводим сообщение об ошибке
        this.$toast.error(`Ошибка: ${error.message}`);
      }
      this.closeDialog();
    },
    closeDialog() {
      this.dialog = false;
    }
  }
}
</script>

<style scoped>

</style>
