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
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>
            Карта
          </v-card-title>
          <v-card-text>
            <GChart
              :settings="{packages: ['geochart'], mapsApiKey: 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'}"
              type="current"
              :data="chartData"
              :options="chartOptions"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
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
          this.predictedRawData=JSON.parse(JSON.stringify(response.data))
          this.rawData=JSON.parse(JSON.stringify(response.data))
          this.getPredictedData()
          this.predictedData = restoreEdgeValues(this.predictedData)
          // this.predictedData = predictValues(this.predictedData)

        })
      apiClient
        .get('plans/')
        .then(response => {
          this.plans=response.data
          this.get_plan_types()
          let sum = this.plans.reduce((accumulator, currentValue) => accumulator + Number(currentValue.price), 0);
          this.averagePrice = sum / this.plans.length;
        })
      apiClient
        .get('users/')
        .then(response => {
          this.users = response.data.results
        })
    },
    computed: {
      chartTimeData: function() {
        const data = [
            ['Абонемент', 'Первая продажа', 'Последняя продажа'],
          ]
        if (this.rawData.length > 1) {
          let first, last, date_start, date_end;
          this.plans.forEach(plan => {
            last = this.rawData.findLast((element) => plan.name === element.plan.name)
            first = this.rawData.findIndex((element) => plan.name === element.plan.name)
            date_start = this.rawData[first].date.split('-')
            date_end = last.date.split('-')
            data.push([
              plan.name,
              new Date(date_start[0], date_start[1], date_start[2]),
              new Date(date_end[0], date_end[1], date_end[2])
            ])
          })
        }
        return data
      },
      chartSankeyData: function() {
        const data = [
            ['Покупатель', 'Toвар', 'Количество продаж'],
          ]
        let count = 0
        this.users.forEach(user => {
          this.plans.forEach(plan => {
            count = this.rawData.filter(value => {
              if (value.user === user.id && value.plan.name === plan.name) {
                return true
              }
            }).length
            data.push([user.username, plan.name, count])
          })
        })

        return data
      },
      chartOrgData: function() {
        const data = [
            ['Name', 'Manager', 'Tooltip'],
            ['Ассортимент', null, 'Типы абонементов'],
          ]
        this.plan_types.forEach(value => {data.push([value, 'Ассортимент', value])})

        this.plans.forEach(value => {data.push([value.name, value.plan_type.name, value.name])})
        return data
      },
      chartCalData: function() {
        const data = [['Date', 'Number of Orders'],]
        let result = Object.values(this.rawData.reduce((r, o) => {
          r[o.date] = r[o.date] || {date: o.date, income : 0, expenses: 0};
          if (o.type == 1) {
            r[o.date].income += 1;
          }
          return r;
        },{}))
        result.forEach(value => {
          let date = value.date.split('-')
          data.push([new Date(date[0], date[1], date[2]), value.income])
        })

        return data
      },
      chartBubbleData: function() {
        let data = [  [ 'Название', 'Цена', 'Число продаж', 'Название', 'Прибыль' ]
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
          products[productName].profit += parseFloat(item.amount)
          products[productName].price = parseFloat(item.amount)
        }

        for (let productName in products) {
          let count = products[productName].count
          let profit = products[productName].profit
          let price = products[productName].price
          if (productName) {
            data.push([productName, price, count, productName, profit])
          }
        }
        return data
      },
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
        users: [],
        averagePrice: 0,
        predictedData: [['Дата', 'Число покупок', 'l=3', 'l=5', 'l=7']],
        predictedRawData: [['Дата', 'Число покупок', 'l=3', 'l=5', 'l=7']],
        rawData: [],
        plans: [],
        plan_types: [],
        chartData: [
          ['Lat', 'Long', 'Name'],
          [37.4232, -122.0853, 'Work'],
        ],
        chartOptions: {
          region: 'russia',
          colorAxis: {colors: ['#00853f', '#e31b23', '#f1bf00']},
          backgroundColor: '#81d4fa',
          datalessRegionColor: '#f8bbd0',
          defaultColor: '#f5f5f5'
        },
        chartTimeOptions: {
          title: 'Product Purchase Timeline',
          height: 300
        },
        chartSankeyOptions: {
          title: 'Sales by Customer and Product',
          height: 1000
        },
        chartOrgOptions: {
          title: 'Assortment Structure',
          allowHtml: true,
          height: 300
        },
        chartCalOptions: {
            title: 'Покупки по дням',
            height: 400,
            width: 1100,
            calendar: {
              cellSize: 20
            }
          },
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
         chartBubbleOptions: {
           title: 'Продажи',
           height: 300,
           hAxis: {
             title: 'Цена'
           },
           vAxis: {
             title: 'Количество продаж'
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
