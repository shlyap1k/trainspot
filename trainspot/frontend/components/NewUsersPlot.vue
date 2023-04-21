<template>
  <div>
    <GChart
      :type="type"
      :data="data"
      :options="options"
    />

    <moving-averages-table
      value-type="Количество новых пользователей"
      table-name="Скользящие средние динамики количества новых пользователей"
      :data="data"
    />
    <GChart :type="type" :data="predictedData" :options="optionsPredicted" />
    <check-hypothesis :data="medianTestResult" v-if="medianTestResult"/>
    <check-hypothesis :data="updownTestResult" v-if="updownTestResult"/>
    <growth-curves :data="data" action-name="Количество новых пользователей"/>
  </div>
</template>

<script>
import { GChart } from 'vue-google-charts/legacy'
import apiClient from '@/src/apiClient'
import MovingAveragesTable from "@/components/MovingAveragesTable.vue";
import restoreEdgeValues from '@/src/restoreEdgeValues'
import predictValues from "@/src/predictValues";
import CheckHypothesis from "@/components/CheckHypothesis.vue";
import _ from 'lodash'
import median_test from "@/src/statistics/statisticsTests/medianTest";
import updownTest from "@/src/statistics/statisticsTests/updownTest";
import GrowthCurves from "@/components/GrowthCurves.vue";
import myCalculateCenteredMovingAverage from "@/src/statistics/utils/calcCenteredMovingAverage";
import centerArray from "@/src/statistics/utils/centerArray";

export default {
  name: "NewUsersPlot",
  components: {
    GChart,
    MovingAveragesTable,
    CheckHypothesis,
    GrowthCurves
  },
  data() {
    return {
      data: [['Дата', 'Количество новых пользователей', 'l=3', 'l=5', 'l=7']],
      predictedData: [['Дата', 'Количество новых пользователей', 'l=3', 'l=5', 'l=7']],
      options: {
        title: 'Динамика регистрации новых пользователей и скользящих средних',
        curveType: 'function',
        legend: {position: 'bottom'},
        height: 500
      },
        optionsPredicted: {
          title: 'Прогноз динамики регистрации новых пользователей и скользящих средних',
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
      .get('users/')
      .then(response => {
        this.rawData = response.data.results
        this.getData()
        this.data = restoreEdgeValues(this.data)
        this.predictedData = predictValues(this.data)
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
        r[o.date_joined] = r[o.date_joined] || {date: o.date_joined, value: 0};
        r[o.date_joined].value += 1;
        return r;
      }, {}))

      result.forEach(r => {
        this.data.push([
          r.date, r.value, null, null, null
        ])
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

