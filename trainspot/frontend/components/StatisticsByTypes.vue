<template>
   <GChart :type="type" :data="data" :options="options" />
</template>

<script>
   import { GChart } from 'vue-google-charts/legacy'
  import apiClient from '@/src/apiClient'
  export default {
    name: "StatisticsByTypes",
    components: {
      GChart
    },
    data() {
      return {
        data: [['Дата']],
        options: {
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        type: 'LineChart',
        rawData: [],
        plan_types: []
      }
    },
    created() {
      apiClient
        .get('financialrecords/')
        .then(response => {
          this.rawData = response.data
          this.get_plan_types()
          this.getData()
        })
    },
    methods: {
      onlyUnique(value, index, array) {
        return array.indexOf(value) === index;
      },
      getData() {
        this.rawData.forEach(function(part, index) {
          this[index].date = this[index].date.split('-');
          this[index].date.pop()
          this[index].date = this[index].date.join('-')
        }, this.rawData);

        let result = Object.values(this.rawData.reduce((r, o) => {
          r[o.date] = r[o.date] || {date: o.date, purchases : []};
          if (o.type == 1) {
            r[o.date].purchases.push({type: o.plan.plan_type.name});
          }
          return r;
        },{}))

        let counts = []

        result.forEach(r => {
          this.plan_types.forEach(pt => {
            counts.push(r.purchases.filter(item => {
              return item.type === pt
            }).length)
          })
          this.data.push([r.date].concat(counts))
          counts = []
        })
        console.log(this.data)
      },
      get_plan_types() {
        this.rawData.map(element => {
          if (element.plan.plan_type) {
            return this.plan_types.push(element.plan.plan_type.name)
          }
        });
        this.plan_types = this.plan_types.filter(this.onlyUnique)
        this.plan_types.map(e => {this.data[0].push(e)})
      }
    }
  }
</script>
