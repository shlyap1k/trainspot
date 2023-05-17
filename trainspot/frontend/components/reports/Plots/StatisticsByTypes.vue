<template>
  <div>
      <v-select
      label="Выбрать тип"
      v-model="selected"
      @change="select"
      :items="data[0].slice(1)"
    ></v-select>
   <GChart :type="type" :data="dataForPlot" :options="options" />
    <moving-averages-table
      value-type="Число покупок"
      table-name="Скользящие средние динамики количества покупок"
      :data="dataForPlot"
    />
    <GChart :type="type" :data="predictedData" :options="optionsPredicted" />
    <check-hypothesis :data="medianTestResult" v-if="medianTestResult"/>
    <check-hypothesis :data="updownTestResult" v-if="updownTestResult"/>
    <growth-curves :data="dataForPlot" :test-results="medianTestResult" action-name="Число покупок" v-if="updownTestResult"/>
  </div>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import apiClient from '@/src/apiClient'
  import MovingAveragesTable from "@/components/reports/Statistics/MovingAveragesTable.vue";
  import restoreEdgeValues from '@/src/restoreEdgeValues'
  import predictValues from "@/src/predictValues";
  import median_test from "@/src/statistics/statisticsTests/medianTest";
  import updownTest from "@/src/statistics/statisticsTests/updownTest";
  import CheckHypothesis from "@/components/reports/Statistics/CheckHypothesis.vue";
  import GrowthCurves from "@/components/reports/Plots/GrowthCurves.vue";
  import myCalculateCenteredMovingAverage from "@/src/statistics/utils/calcCenteredMovingAverage";
  import centerArray from "@/src/statistics/utils/centerArray";
  export default {
    name: "StatisticsByTypes",
    components: {
      GChart,
      MovingAveragesTable,
      CheckHypothesis,
      GrowthCurves
    },
    data() {
      return {
        selected: null,
        medianTestResult: null,
        updownTestResult: null,
        predictedData: null,
        data: [['Дата']],
        dataForPlot: [['Дата']],
        // predictedData: [['Дата', 'Число покупок', 'l=3', 'l=5', 'l=7']],
        options: {
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        optionsPredicted: {
          title: 'Прогноз динамики количества продаж абонементов выбранного типа',
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        type: 'LineChart',
        rawData: [],
        plan_types: [],
        plotData: []
      }
    },
    created() {
      apiClient
        .get('financialrecords/')
        .then(response => {
          this.rawData = response.data
          this.get_plan_types()
          this.getData()
          this.select()
        })
    },
    methods: {
      select() {
        const index = this.data[0].indexOf(this.selected)
        const data = [ [this.data[0][0], this.data[0][index], 'l=3', 'l=5', 'l=7'] ]
        this.data.slice(1).forEach(value => {
          data.push([value[0], value[index], 0, 0, 0])
        })
        let l3 = centerArray(myCalculateCenteredMovingAverage(data.slice(1), 3));
        let l5 = centerArray(myCalculateCenteredMovingAverage(data.slice(1), 5));
        let l7 = centerArray(myCalculateCenteredMovingAverage(data.slice(1), 7));
        for (let i = 0; i < data.length-1; i++) {
          data[i + 1][2] = l3[i];
          data[i + 1][3] = l5[i];
          data[i + 1][4] = l7[i];
        }
        this.dataForPlot = data
        this.dataForPlot = restoreEdgeValues(this.dataForPlot)
        this.predictedData = predictValues(this.dataForPlot)
        this.updownTestResult = updownTest(this.dataForPlot.slice(1).map(row => row[1]))
        this.medianTestResult = median_test(this.dataForPlot.slice(1).map(row => row[1]))

      },
      filterBySelected() {
        const index = this.data[0].indexOf(this.selected)

      },
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
        this.selected = this.data[0][1]
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
