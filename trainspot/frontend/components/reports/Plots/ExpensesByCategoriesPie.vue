<template>
  <v-card>
    <v-card-title>
      Соотношение затрат на различные категории
    </v-card-title>
    <v-card-text>
      <GChart :type="type" :data="data" :options="options" />
    </v-card-text>
  </v-card>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy';
  import apiClient from "@/src/apiClient";
  export default {
    name: "ExpensesByCategoriesPie",
    components: {
      GChart
    },
    data() {
      return {
        type: 'PieChart',
        data: [
          ['Тип абонемента', 'Потрачено денег'],
        ],
        options: {
          height: 400,
        },
        rawData: null
      };
    },
    created() {
      apiClient
        .get('financialrecords/')
        .then(response => {
          this.rawData = response.data
          this.getData()
        })
    },
    methods: {
      getData() {
        let result = Object.values(this.rawData.reduce((r, o) => {
          r[o.plan.plan_type.name] = r[o.plan.plan_type.name] || {type: o.plan.plan_type.name, amount : 0};
          r[o.plan.plan_type.name].amount += +o.amount;
          return r;
        },{}))
        result.forEach(r => {
          this.data.push([r.type, r.amount])
        })
      }
    }
  }
</script>
