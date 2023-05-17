<template>
  <v-card class="pa-2">
    <v-card-text>
      <GChart
        :settings="{packages: ['calendar']}"
        type="Calendar"
        :data="chartCalData"
        :options="chartCalOptions"
      />
    </v-card-text>
  </v-card>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  export default {
    name: "PurchasesCalendar",
    components: {
      GChart
    },
    props: {
      rawData: {
        type: Array,
        required: true
      }
    },
    computed: {
      chartCalData: function () {
        const data = [['Date', 'Number of Orders'],]
        let result = Object.values(this.rawData.reduce((r, o) => {
          r[o.date] = r[o.date] || {date: o.date, income: 0, expenses: 0};
          if (o.type == 1) {
            r[o.date].income += 1;
          }
          return r;
        }, {}))
        result.forEach(value => {
          let date = value.date.split('-')
          data.push([new Date(date[0], date[1], date[2]), value.income])
        })

        return data
      }
    },
    data() {
      return {
        chartCalOptions: {
          title: 'Покупки по дням',
          height: 400,
          width: 1100,
          calendar: {
            cellSize: 20
          }
        }
      }
    }
  }
</script>

<style scoped>

</style>
