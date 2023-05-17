<template>
  <v-card class="pa-2">
    <v-card-title>
      Диаграмма областей
    </v-card-title>
    <v-card-text>
      <GChart
        type="AreaChart"
        :data="chartAreaData"
        :options="chartAreaOptions"
      />
    </v-card-text>
  </v-card>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import centerArray from "@/src/statistics/utils/centerArray";
  import myCalculateCenteredMovingAverage from "@/src/statistics/utils/calcCenteredMovingAverage";
  import restoreEdgeValues from "@/src/restoreEdgeValues";
  export default {
    name: "ProfitAndPredictedProfitDiagram",
    components: {
      GChart
    },
    props: {
      plans: {
        type: Array,
        required: true
      },
      rawData: {
        type: Array,
        required: true
      }
    },
    created() {
      let sum = this.plans.reduce((accumulator, currentValue) => accumulator + Number(currentValue.price), 0);
      this.averagePrice = sum / this.plans.length;
      console.log(this.plans)
      this.predictedRawData=JSON.parse(JSON.stringify(this.rawData))
      this.getPredictedData()
      this.predictedData = restoreEdgeValues(this.predictedData)
    },
    computed: {
      chartAreaData: function() {
        let i = 0
        const data = [['Year', 'Доход', 'Предполагаемый доход']]
        const rawData = JSON.parse(JSON.stringify(this.rawData))
        rawData.forEach(function(part, index) {
          this[index].date = this[index].date.split('-');
          this[index].date.pop()
          this[index].date = this[index].date.join('-')
        }, rawData);
        let result = Object.values(rawData.reduce((r, o) => {
          r[o.date] = r[o.date] || {date: o.date, income : 0, expenses: 0};
          if (o.type == 1) {
            r[o.date].income += +o.amount;
          } else if (o.type == 2) {
            r[o.date].expenses += +o.amount;
          }
          return r;
        },{}))
        if (this.predictedData.length > 1) {
          result.forEach(r => {
            data.push([r.date, r.income, this.averagePrice * this.predictedData[i+1][3]])
            i = i + 1
          })
        } else {
          result.forEach(r => {
            data.push([r.date, r.income, 0])
            i++
          })
        }
        return data
      }
    },
    methods: {
      getPredictedData() {
        this.predictedRawData.forEach(function(part, index) {
          this[index].date = this[index].date.split('-');
          this[index].date.pop()
          this[index].date = this[index].date.join('-')
        }, this.predictedRawData);
        let result = Object.values(this.predictedRawData.reduce((r, o) => {
          r[o.date] = r[o.date] || {date: o.date, value : 0};
          if (o.type == 1) {
            r[o.date].value += 1;
          }
          return r;
        },{}))
        let prev = null
        let first = result ? result[0] : null
        result.forEach(r => {
          this.predictedData.push([
            r.date, r.value, 0, 0, 0
          ])
          prev = r
        })
        let l3 = centerArray(myCalculateCenteredMovingAverage(this.predictedData.slice(1), 3));
        let l5 = centerArray(myCalculateCenteredMovingAverage(this.predictedData.slice(1), 5));
        let l7 = centerArray(myCalculateCenteredMovingAverage(this.predictedData.slice(1), 7));
        for (let i = 0; i < result.length-1; i++) {
          this.predictedData[i + 1][2] = l3[i];
          this.predictedData[i + 1][3] = l5[i];
          this.predictedData[i + 1][4] = l7[i];
        }
      },
    },
    data() {
      return {
        averagePrice: 0,
        predictedData: [['Дата', 'Число покупок', 'l=3', 'l=5', 'l=7']],
        predictedRawData: [['Дата', 'Число покупок', 'l=3', 'l=5', 'l=7']],
        chartAreaOptions: {
          title: '',
          hAxis: {
            title: 'Дата'
          },
          vAxis: {
            title: 'Размер'
          },
          height: 300
        }
      }
    }
  }
</script>

