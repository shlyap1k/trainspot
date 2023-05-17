<template>
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
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  export default {
    name: "SellsAndProfitBubbleDiagram",
    components: {
      GChart
    },
    props: {
      rawData: {
        type: Array,
        required: true
      }
    },
    computed: {
      chartBubbleData: function () {
        let data = [['Название', 'Цена', 'Число продаж', 'Название', 'Прибыль']
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
    },
    data() {
      return {
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
