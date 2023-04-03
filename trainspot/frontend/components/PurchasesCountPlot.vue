<template>
  <GChart :type="type" :data="data" :options="options" />
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import apiClient from '@/src/apiClient'
  export default {
    name: "PurchasesCountPlot",
    components: {
      GChart
    },
    data() {
      return {
        data: [['Дата', 'Число покупок']],
        options: {
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        type: 'LineChart',
        rawData: []
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
        this.rawData.forEach(function(part, index) {
          this[index].date = this[index].date.split('-');
          this[index].date.pop()
          this[index].date = this[index].date.join('-')
        }, this.rawData);
        let result = Object.values(this.rawData.reduce((r, o) => {
          r[o.date] = r[o.date] || {date: o.date, purchases : 0};
          if (o.type == 1) {
            r[o.date].purchases += 1;
          }
          return r;
        },{}))
        let prev = null
        let first = result ? result[0] : null
        result.forEach(r => {
          this.data.push([
            r.date, r.purchases
          ])
          prev = r
        })
      }
    }
  }
</script>
