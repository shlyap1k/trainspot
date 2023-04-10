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
