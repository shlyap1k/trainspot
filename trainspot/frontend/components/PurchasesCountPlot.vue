<template>
  <div>
    <GChart :type="type" :data="data" :options="options" />
    <moving-averages-table
      value-type="Число покупок"
      table-name="Скользящие средние динамики количества покупок"
      :data="data"
    />
    <GChart :type="type" :data="predictedData" :options="optionsPredicted" />
  </div>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import MovingAveragesTable from "@/components/MovingAveragesTable.vue";
  import apiClient from '@/src/apiClient'
  import restoreEdgeValues from '@/src/restoreEdgeValues'
  import predictValues from "@/src/predictValues";
  export default {
    name: "PurchasesCountPlot",
    components: {
      GChart,
      MovingAveragesTable
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
    created() {
      apiClient
        .get('financialrecords/')
        .then(response => {
          this.rawData = response.data
          this.getData()
          this.data = restoreEdgeValues(this.data)
          this.predictedData = predictValues(this.data)
          console.table(this.data)
          console.table(this.predictedData)
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
        let l3 = this.centerArray(this.myCalculateCenteredMovingAverage(result, 3));
        let l5 = this.centerArray(this.myCalculateCenteredMovingAverage(result, 5));
        let l7 = this.centerArray(this.myCalculateCenteredMovingAverage(result, 7));
        for (let i = 0; i < result.length; i++) {
          this.data[i + 1][2] = l3[i];
          this.data[i + 1][3] = l5[i];
          this.data[i + 1][4] = l7[i];
        }
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
            sum += data[j].value;
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
      }
    }
  }
</script>
