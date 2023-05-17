<template>
  <v-card>
    <v-card-title>
      Диаграмма Санки
    </v-card-title>
    <v-card-text>
      <GChart
        :settings="{packages: ['sankey']}"
        type="Sankey"
        :data="chartSankeyData"
        :options="chartSankeyOptions"
      />
    </v-card-text>
  </v-card>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  export default {
    name: "SankeyDiagram",
    components: {
      GChart
    },
    props: {
      users: {
        type: Array,
        required: true
      },
      plans: {
        type: Array,
        required: true
      },
      rawData: {
        type: Array,
        required: true
      }
    },
    computed: {
      chartSankeyData: function () {
        const data = [
          ['Покупатель', 'Toвар', 'Количество продаж'],
        ]
        let count = 0
        this.users.forEach(user => {
          this.plans.forEach(plan => {
            count = this.rawData.filter(value => {
              if (value.user === user.id && value.plan.name === plan.name) {
                return true
              }
            }).length
            data.push([user.username, plan.name, count])
          })
        })
        return data
      }
    },
    data() {
      return {
        chartSankeyOptions: {
          title: 'Sales by Customer and Product',
          height: 1000
        }
      }
    }
  }
</script>

<style scoped>

</style>
