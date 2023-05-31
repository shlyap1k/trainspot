<template>
  <div>
    <v-select
      label="Выбрать тип"
      v-model="selected"
      @change="select"
      :items="plan_types"
      v-if="selecting"
    ></v-select>
    <GChart :type="type" :data="data" :options="options" />
    <moving-averages-table
      value-type="Число покупок"
      table-name="Скользящие средние динамики количества покупок"
      :data="data"
    />
    <GChart :type="type" :data="predictedData" :options="optionsPredicted" />
    <check-hypothesis :data="medianTestResult" v-if="medianTestResult"/>
    <check-hypothesis :data="updownTestResult" v-if="updownTestResult"/>
    <growth-curves :data="data" :test-results="medianTestResult" action-name="Число покупок" v-if="medianTestResult"/>
  </div>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import MovingAveragesTable from "@/components/reports/Statistics/MovingAveragesTable.vue";
  import apiClient from '@/src/apiClient'
  import restoreEdgeValues from '@/src/restoreEdgeValues'
  import predictValues from "@/src/predictValues";
  import median_test from "@/src/statistics/statisticsTests/medianTest";
  import updownTest from "@/src/statistics/statisticsTests/updownTest";
  import CheckHypothesis from "@/components/reports/Statistics/CheckHypothesis.vue";
  import GrowthCurves from "@/components/reports/Plots/GrowthCurves.vue";
  import myCalculateCenteredMovingAverage from "@/src/statistics/utils/calcCenteredMovingAverage";
  import centerArray from "@/src/statistics/utils/centerArray";
  export default {
    name: "PredictedStatisticsPage",
    components: {
      GChart,
      MovingAveragesTable,
      CheckHypothesis,
      GrowthCurves,
    },
    props: {
      statsName: {
        type: String,
        required: true,
      },
      apiUrl: {
        type: String,
        required: true,
      },
      tableName: {
        type: String,
        required: true,
      },
      valueType: {
        type: String,
        required: true,
      },
      byMonth: {
        type: Boolean,
        required: true
      },
      selecting: {
        type: Boolean,
        required: false
      }
    },
    data() {
      return {
        selected: null,
        data: [['Дата', this.valueType, 'l=3', 'l=5', 'l=7']],
        predictedData: [['Дата', 'Число покупок', 'l=3', 'l=5', 'l=7']],
        options: {
          title: `Динамика ${this.statsName} и скользящих средних`,
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        optionsPredicted: {
          title: `Прогноз динамики ${this.statsName}`,
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        type: 'LineChart',
        rawData: [],
        plan_types: [],
      }
    },
    computed: {
      medianTestResult: function () {
        if (this.data.length > 1) {
          return median_test(this.data.slice(1).map(row => row[1]))
        } else {
          return null
        }
      },
      updownTestResult: function () {
        return updownTest(this.data.slice(1).map(row => row[1]))
      }
    },
    created() {
      apiClient
        .get(this.apiUrl)
        .then(response => {
          if (response.data.results) {
            this.rawData = response.data.results
          } else {
            this.rawData = response.data
          }
          if (this.selecting) {
            this.get_plan_types()
            this.getData()
            this.select()
          } else {
            this.getData()
          }
          this.data = restoreEdgeValues(this.data)
          this.predictedData = predictValues(this.data)
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
      get_plan_types() {
        this.rawData.map(element => {
          if (element.plan.plan_type) {
            return this.plan_types.push(element.plan.plan_type.name)
          }
        });
        this.plan_types = this.plan_types.filter(this.onlyUnique)
        this.plan_types.map(e => {this.data[0].push(e)})
      },
      getData() {
        if (this.byMonth) {

          this.rawData.forEach(function (part, index) {
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

        } else if (this.selecting) {

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

        } else {
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
        }
      },
    }
  }
</script>
