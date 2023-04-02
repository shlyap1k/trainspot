<template>
  <v-card>
    <v-card-title>
      Доходы и расходы
    </v-card-title>
    <GChart :type="type" :data="data" :options="options" />
  </v-card>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import apiClient from '@/src/apiClient'
  export default {
    name: "ProfitPlot",
    components: {
      GChart
    },
    props: {
      // profit: {
      //   type: Array,
      //   required: true
      // }
    },
    data() {
      return {
        type: 'LineChart',
        data: [
          ['Дата', 'Доходы', 'Расходы'],
        ],
        options: {
          curveType: 'function',
          legend: { position: 'bottom' },
          height: 500
        },
        rawData: null
      }
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
        console.log(this.rawData)
        this.rawData.forEach(function(part, index) {
          this[index].date = this[index].date.split('-');
          this[index].date.pop()
          this[index].date = this[index].date.join('-')
        }, this.rawData);
        let result = Object.values(this.rawData.reduce((r, o) => {
          r[o.date] = r[o.date] || {date: o.date, income : 0, expenses: 0};
          if (o.type == 1) {
            r[o.date].income += +o.amount;
          } else if (o.type == 2) {
            r[o.date].expenses += +o.amount;
          }
          return r;
        },{}))
        console.log(result)

        console.log(this.data)
        result.forEach(r => {
          this.data.push([r.date, r.income, r.expenses])
        })
      }
    }
  }
</script>
