<template>
  <GChart :type="type" :data="data" :options="options" />
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import apiClient from '@/src/apiClient'
  export default {
    name: "NewUsersPlot",
    components: {
      GChart
    },
    data() {
      return {
        data: [['Дата', 'Количество новых пользователей']],
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
        .get('users/')
        .then(response => {
          this.rawData = response.data.results
          this.getData()
        })
    },
    methods: {
      getData() {
        this.rawData.forEach(function(part, index) {
          this[index].date_joined = this[index].date_joined.split('T');
          this[index].date_joined.pop()
          this[index].date_joined = this[index].date_joined.join('-')
        }, this.rawData);

        let result = Object.values(this.rawData.reduce((r, o) => {
          r[o.date_joined] = r[o.date_joined] || {date: o.date_joined, newUsersCount: 0};
          r[o.date_joined].newUsersCount += 1;
          return r;
        }, {}))

        result.forEach(r => {
          this.data.push([
            r.date, r.newUsersCount
          ])
        })

      }
    }
  }
</script>

