<template>
  <div>
    <GChart :type="type" :data="data" :options="options" />
    <moving-averages-table
      value-type="Число покупок"
      table-name="Скользящие средние динамики количества покупок"
      :data="data"
    />
    <GChart :type="type" :data="predictedData" :options="optionsPredicted" />
    <check-hypothesis :data="medianTestResult" v-if="medianTestResult"/>
    <check-hypothesis :data="updownTestResult" v-if="updownTestResult"/>
    <growth-curves :data="data" action-name="Число покупок"/>
  </div>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import MovingAveragesTable from "@/components/MovingAveragesTable.vue";
  import apiClient from '@/src/apiClient'
  import restoreEdgeValues from '@/src/restoreEdgeValues'
  import predictValues from "@/src/predictValues";
  import median_test from "@/src/statistics/statisticsTests/medianTest";
  import updownTest from "@/src/statistics/statisticsTests/updownTest";
  import CheckHypothesis from "@/components/CheckHypothesis.vue";
  import GrowthCurves from "@/components/GrowthCurves.vue";
  import myCalculateCenteredMovingAverage from "@/src/statistics/utils/calcCenteredMovingAverage";
  import centerArray from "@/src/statistics/utils/centerArray";
  export default {
    name: "PurchasesCountPlot",
    components: {
      GChart,
      MovingAveragesTable,
      CheckHypothesis,
      GrowthCurves
    },
    data() {
      return {
        data: [['Дата', 'Число покупок', 'l=3', 'l=5', 'l=7']],
        predictedData: [['Дата', 'Число покупок', 'l=3', 'l=5', 'l=7']],
        options: {
          title: 'Динамика количества продаж и скользящих средних',
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        optionsPredicted: {
          title: 'Прогноз динамики количества продаж и скользящих средних',
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        type: 'LineChart',
        rawData: []
      }
    },
    computed: {
      medianTestResult: function () {
        if (this.data.length > 1) {
          return median_test(this.data)
        } else {
          return null
        }
      },
      updownTestResult: function () {
        // console.log(this.data)
        return updownTest(this.data)
      }
    },
    created() {
      apiClient
        .get('financialrecords/')
        .then(response => {
          this.rawData = response.data
          this.getData()
          this.data = restoreEdgeValues(this.data)
          this.predictedData = predictValues(this.data)
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
          r[o.date] = r[o.date] || {date: o.date, value : 0};
          if (o.type == 1) {
            r[o.date].value += 1;
          }
          return r;
        },{}))
        let prev = null
        let first = result ? result[0] : null
        result.forEach(r => {
          this.data.push([
            r.date, r.value, 0, 0, 0
          ])
          prev = r
        })
        let l3 = centerArray(myCalculateCenteredMovingAverage(this.data.slice(1), 3));
        let l5 = centerArray(myCalculateCenteredMovingAverage(this.data.slice(1), 5));
        let l7 = centerArray(myCalculateCenteredMovingAverage(this.data.slice(1), 7));
        for (let i = 0; i < result.length; i++) {
          this.data[i + 1][2] = l3[i];
          this.data[i + 1][3] = l5[i];
          this.data[i + 1][4] = l7[i];
        }
      },
    }
  }
</script>
