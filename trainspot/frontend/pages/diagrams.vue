<template>
  <v-container class="grey lighten-5">
    <v-row>
      <v-col cols="6">
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
      </v-col>
      <v-col cols="6">
        <v-card class="pa-2">
          <v-card-title>
            Пузырьковая диаграмма
          </v-card-title>
          <v-card-text>
            <GChart
              type="BubbleChart"
              :data="chartBubbleData"
              :options="chartBubbleOptions"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col sm="12">
        <v-card class="pa-2">
          <v-card-text>
            <GChart
              :settings="{packages: ['calendar']}"
              type="Calendar"
              :data="chartCalData"
              :options="chartCalOptions"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>
            Организационная диаграмма
          </v-card-title>
          <v-card-text align="center">
              <GChart
                :settings="{packages: ['orgchart']}"
                type="OrgChart"
                :data="chartOrgData"
                :options="chartOrgOptions"
              />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>
            Диаграмма Санки
          </v-card-title>
          <v-card-text>
            <GChart
              :settings="{packages: ['sankey']}"
              type="Sankey"
              :data="chartSankeyData"
              :options="chartSankeyOptions"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>
            Хронология продаж
          </v-card-title>
          <v-card-text>
            <GChart
              :settings="{packages: ['timeline']}"
              type="Timeline"
              :data="chartTimeData"
              :options="chartTimeOptions"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
<!--    {{timeData}}-->

<!--    абонементы-->
<!--    {{plan_types}}-->
    {{predictedData}}
  </v-container>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import apiClient from '@/src/apiClient'
  import centerArray from "@/src/statistics/utils/centerArray";
  import myCalculateCenteredMovingAverage from "@/src/statistics/utils/calcCenteredMovingAverage";
  import restoreEdgeValues from "@/src/restoreEdgeValues";
  import predictValues from "@/src/predictValues";
  export default {
    components: {
      GChart
    },
    name: "",
    mounted() {
      apiClient
        .get('financialrecords/')
        .then(response => {
          // console.log(response.data)
          this.predictedRawData=JSON.parse(JSON.stringify(response.data))
          this.rawData=JSON.parse(JSON.stringify(response.data))
          this.getPredictedData()
          this.predictedData = restoreEdgeValues(this.predictedData)
          // this.predictedData = predictValues(this.predictedData)

        })
      // apiClient
      //   .get('financialrecords/')
      //   .then(response => {
      //     this.rawData=response.data
      //   })
      apiClient
        .get('plans/')
        .then(response => {
          this.plans=response.data
          this.get_plan_types()
          let sum = this.plans.reduce((accumulator, currentValue) => accumulator + Number(currentValue.price), 0);
          this.averagePrice = sum / this.plans.length;
          // console.log(this.chartAreaData)
        })
    },
    computed: {
      chartBubbleData: function() {
        // [
        //    ['ID', 'X', 'Y', 'Temperature'],
        //    ['001', 80, 167, 120],
        //    ['002', 79, 136, 130],
        //    ['003', 78, 184, 50],
        //    ['004', 72, 278, 230],
        //    ['005', 81, 200, 210],
        //    ['006', 72, 170, 100]
        //  ]
        let data = [  ['Цена', 'Число продаж', 'Прибыль', 'Название']
        ]

        let products = {}

        for (let i = 0; i < this.rawData.length; i++) {
          let item = this.rawData[i]
          let productName = item.plan.name

          if (!products[productName]) {
            products[productName] = {
              count: 0,
              profit: 0
            }
          }

          products[productName].count++
          products[productName].profit += parseFloat(item.plan.price)
          products[productName].price = parseFloat(item.plan.price)
        }

        for (let productName in products) {
          let count = products[productName].count
          let profit = products[productName].profit
          let price = products[productName].plan
          console.log(products[productName])
          data.push([String(price), count, profit, productName])
        }
        console.log(data)
        return data
      },
      chartAreaData: function() {
        let i = 0
        const data = [['Year', 'Доход', 'Предполагаемый доход']]
        this.rawData.forEach(function(part, index) {
          this[index].date = this[index].date.split('-');
          this[index].date.pop()
          this[index].date = this[index].date.join('-')
        }, this.rawData);
        let result = Object.values(this.rawData.reduce((r, o) => {
          r[o.date] = r[o.date] || {date: o.date, income : 0, expenses: 0};
          if (o.type == 1) {
            r[o.date].income += +o.amount;
          } else if (o.type == 2) {
            r[o.date].expenses += +o.amount;
          }
          return r;
        },{}))
        console.log(this.predictedData)
        console.log(result)
        if (this.predictedData.length > 1) {
          result.forEach(r => {
            data.push([r.date, r.income, this.averagePrice * this.predictedData[i+1][3]])
            console.log(i, r.income, this.predictedData[i+1][3])
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
      get_plan_types() {
        this.plans.map(element => {
          return this.plan_types.push(element.plan_type.name)
        });
        this.plan_types = this.plan_types.filter((value, index) => this.plan_types.indexOf(value) === index)
      },
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
        rawData: [],
        plans: [],
        plan_types: [],
        chartTimeData: [
            ['Product', 'Start', 'End'],
            ['Product A', new Date(2023, 3, 1), new Date(2023, 4, 1)],
            ['Product B', new Date(2023, 2, 1), new Date(2023, 5, 1)],
            ['Product C', new Date(2023, 1, 1), new Date(2023, 4, 1)]
          ],
          chartTimeOptions: {
            title: 'Product Purchase Timeline',
            height: 300
          },
         chartSankeyData: [
            ['From', 'To', 'Number of Sales'],
            ['Customer 1', 'Product A', 10],
            ['Customer 1', 'Product B', 5],
            ['Customer 2', 'Product A', 15],
            ['Customer 2', 'Product C', 20],
            ['Customer 3', 'Product B', 7],
            ['Customer 3', 'Product C', 12],
            ['Customer 4', 'Product A', 8],
            ['Customer 4', 'Product B', 6],
            ['Customer 4', 'Product C', 4]
          ],
          chartSankeyOptions: {
            title: 'Sales by Customer and Product',
            height: 300
          },
         chartOrgData: [
            ['Name', 'Manager', 'Tooltip'],
            ['Assortment', null, 'Assortment of goods'],
            ['Category A', 'Assortment', 'Category A products'],
            ['Category B', 'Assortment', 'Category B products'],
            ['Product 1', 'Category A', 'Product 1'],
            ['Product 2', 'Category A', 'Product 2'],
            ['Product 3', 'Category B', 'Product 3'],
            ['Product 4', 'Category B', 'Product 4']
          ],
          chartOrgOptions: {
            title: 'Assortment Structure',
            allowHtml: true,
            height: 300
          },
         chartCalData: [
            ['Date', 'Number of Orders'],
            [new Date(2023, 5, 4), 12],
            [new Date(2023, 5, 5), 8],
            [new Date(2023, 5, 6), 15],
            [new Date(2023, 5, 7), 20],
            [new Date(2023, 5, 8), 10],
            [new Date(2023, 5, 9), 5]
          ],
          chartCalOptions: {
            title: 'Orders per Day',
            height: 300,
            width: 1100,
            calendar: {
              cellSize: 20
            }
          },
         // chartAreaData: [
         //    ['Year', 'Доход', 'Предполагаемый доход'],
         //    // ['2015', 500, 300],
         //    // ['2016', 600, 400],
         //    // ['2017', 700, 500],
         //    // ['2018', 800, 600]
         //  ],
          chartAreaOptions: {
            title: '',
            hAxis: {
              title: 'Дата'
            },
            vAxis: {
              title: 'Размер'
            },
            height: 300
          },
         // chartBubbleData: [
         //   ['ID', 'X', 'Y', 'Temperature'],
         //   ['001', 80, 167, 120],
         //   ['002', 79, 136, 130],
         //   ['003', 78, 184, 50],
         //   ['004', 72, 278, 230],
         //   ['005', 81, 200, 210],
         //   ['006', 72, 170, 100]
         // ],
         chartBubbleOptions: {
           title: 'Продажи',
           hAxis: {
             title: 'Цена'
           },
           vAxis: {
             title: 'Количество клиентов, купивших товар'
           },
           bubble: {
             textStyle: {
               fontSize: 11
             }
           }
         }
       }
     }
  }
</script>

<style scoped>

</style>
