<template>
  <div>
    <v-select
      label="Выбрать тип"
      v-model="type_id"
      :items="plan_types"
      @change="test"
    ></v-select>
    <GChart
      type="ColumnChart"
      :data="chartData"
      :options="chartOptions"
    />
<!--    {{test()}}-->
<!--    {{get_plan_types()}}-->
  </div>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  // import apiClient from "@/src/apiClient";
  export default {
    name: "PriceListCharts",
    components: {
      GChart
    },
    props: {
      plans: {
        type: Array,
        required: true
      }
    },
    data () {
      return {
        chartData: [
          ['Название', 'Цена']
        ],
        chartOptions: {
          chart: {
            title: 'Company Performance',
            subtitle: 'Sales, Expenses, and Profit: 2014-2017',
          }
        },
        plan_types: [],
        type_id: null
      }
    },
    watch: {
      plans: {
        handler () {
          this.get_plan_types()
          if (this.plan_types) {
            this.type_id = this.plan_types[0]
            this.test()
          }
        },
        deep: 1
      }
    },
    created() {

    },
    methods: {
      test() {
        this.chartData = [ ['Название', 'Цена'] ]
        const filtered = this.plans.filter(plan => plan.plan_type.name === this.type_id)
        filtered.map(f => this.chartData.push([f.name, Number(f.price)]))
      },
      get_plan_types() {

        this.plans.map(element => {
          return this.plan_types.push(element.plan_type.name)
        });
      }
    }
  }
</script>
