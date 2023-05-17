<template>
  <v-card>
    <v-card-title>
      Хронология продаж
    </v-card-title>
    <v-card-text>
      <GChart
        :settings="{packages: ['timeline']}"
        type="Timeline"
        :data="chartTimeData"
        :options="chartTimeOptions"
      />
    </v-card-text>
  </v-card>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  export default {
    name: "SellsTimeline",
    components: {
      GChart
    },
    props: {
      rawData: {
        type: Array,
        required: true
      },
      plans: {
        type: Array,
        required: true
      }
    },
    computed: {
      chartTimeData: function () {
        const data = [
          ['Абонемент', 'Первая продажа', 'Последняя продажа'],
        ]
        if (this.rawData.length > 1) {
          let first, last, date_start, date_end;
          this.plans.forEach(plan => {
            last = this.rawData.findLast((element) => plan.name === element.plan.name)
            first = this.rawData.findIndex((element) => plan.name === element.plan.name)
            date_start = this.rawData[first].date.split('-')
            date_end = last.date.split('-')
            data.push([
              plan.name,
              new Date(date_start[0], date_start[1], date_start[2]),
              new Date(date_end[0], date_end[1], date_end[2])
            ])
          })
        }
        return data
      }
    },
    data() {
      return {
        chartTimeOptions: {
          title: 'Product Purchase Timeline',
          height: 300
        },
      }
    }
  }
</script>

<style scoped>

</style>
