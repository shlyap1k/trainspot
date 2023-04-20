<template>
  <div>
    {{data}}
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
    <growth-curves :data="dataForPlot" action-name="Число покупок"/>
  </div>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import apiClient from '@/src/apiClient'
  import MovingAveragesTable from "@/components/MovingAveragesTable.vue";
  import restoreEdgeValues from '@/src/restoreEdgeValues'
  import predictValues from "@/src/predictValues";
  import median_test from "@/src/statistics/statisticsTests/medianTest";
  import updownTest from "@/src/statistics/statisticsTests/updownTest";
  import CheckHypothesis from "@/components/CheckHypothesis.vue";
  import GrowthCurves from "@/components/GrowthCurves.vue";
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
        })
    },
    computed: {
      medianTestResult: function () {
        if (this.data.length > 1) {
          return median_test(this.data)
        } else {
          return null
        }
      },
      // updownTestResult: function () {
      //   // console.log(this.data)
      //   return updownTest(this.data)
      // },
      // predictedData: function () {
      //   this.dataForPlot = restoreEdgeValues(this.dataForPlot)
      //   return predictValues(this.dataForPlot)
      // },
      // dataForPlot: function() {
      //   const index = this.data[0].indexOf(this.selected)
      //   const data = [ [this.data[0][0], this.data[0][index], 'l=3', 'l=5', 'l=7'] ]
      //   this.data.slice(1).forEach(value => {
      //     data.push([value[0], value[index], 0, 0, 0])
      //   })
      //   let l3 = this.centerArray(this.myCalculateCenteredMovingAverage(data, 3));
      //   let l5 = this.centerArray(this.myCalculateCenteredMovingAverage(data, 5));
      //   let l7 = this.centerArray(this.myCalculateCenteredMovingAverage(data, 7));
      //   console.log(data)
      //   for (let i = 0; i < data.length-1; i++) {
      //     console.log(data.length, i+1)
      //     data[i + 1][2] = l3[i];
      //     data[i + 1][3] = l5[i];
      //     data[i + 1][4] = l7[i];
      //   }
      //   return data
      // }
    },
    methods: {
      select() {
        const index = this.data[0].indexOf(this.selected)
        const data = [ [this.data[0][0], this.data[0][index], 'l=3', 'l=5', 'l=7'] ]
        this.data.slice(1).forEach(value => {
          data.push([value[0], value[index], 0, 0, 0])
        })
        let l3 = this.centerArray(this.myCalculateCenteredMovingAverage(data, 3));
        let l5 = this.centerArray(this.myCalculateCenteredMovingAverage(data, 5));
        let l7 = this.centerArray(this.myCalculateCenteredMovingAverage(data, 7));
        console.log(data)
        for (let i = 0; i < data.length-1; i++) {
          console.log(data.length, i+1)
          data[i + 1][2] = l3[i];
          data[i + 1][3] = l5[i];
          data[i + 1][4] = l7[i];
        }
        this.dataForPlot = data
        this.dataForPlot = restoreEdgeValues(this.dataForPlot)
        this.predictedData = predictValues(this.dataForPlot)
        this.updownTestResult = updownTest(this.dataForPlot)
        this.medianTestResult = median_test(this.dataForPlot)

      },
      myCalculateCenteredMovingAverage(data, windowSize) {
        const result = [];
        for (let k = 0; k < data.length; k++) {
          result[k] = null
        }
        const dataLength = data.length;
        let index = 0;
        for (let i = Math.floor(windowSize / 2); i < dataLength - Math.floor(windowSize / 2); i++) {
          let sum = 0;
          for (let j = i - Math.floor(windowSize / 2); j <= i + Math.floor(windowSize / 2); j++) {
            sum += data[j][1];
            index = j
          }
          result[index-1] = sum / windowSize;
        }
        return result;
      },
      centerArray(arr) {
        let startCount = 0; // количество null в начале массива
        let endCount = 0; // количество null в конце массива

        // Проверяем наличие null в массиве
        if (!arr.includes(null)) {
          return arr;
        }

        // Подсчитываем количество null в начале массива
        for (let i = 0; i < arr.length; i++) {
          if (arr[i] === null) {
            startCount++;
          } else {
            break; // выходим из цикла, если находим первый не null элемент
          }
        }

        // Подсчитываем количество null в конце массива
        for (let i = arr.length - 1; i >= 0; i--) {
          if (arr[i] === null) {
            endCount++;
          } else {
            break; // выходим из цикла, если находим первый не null элемент
          }
        }

        // Если количество null в начале и в конце массива уже равно или разница между ними не превышает 1, возвращаем исходный массив
        if (startCount === endCount || Math.abs(startCount - endCount) <= 1) {
          return arr;
        }

        // Если количество null в начале больше, выкидываем null из начала и вставляем их в конец массива
        if (startCount > endCount) {
          while (startCount > endCount + 1) {
            arr.push(null); // добавляем null в конец массива
            arr.shift(); // удаляем null из начала массива
            startCount--;
            endCount++;
          }
        }
        // Если количество null в конце больше, выкидываем null из конца и вставляем их в начало массива
        else {
          while (endCount > startCount + 1) {
            arr.unshift(null); // добавляем null в начало массива
            arr.pop(); // удаляем null из конца массива
            endCount--;
            startCount++;
          }
        }

        // Возвращаем выровненный массив
        return arr;
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
