<template>
  <v-card>
    <v-card-title>
      Статистические показатели динамики
    </v-card-title>
    <v-card-text>
      <v-simple-table>
        <thead>
          <tr>
            <th class="text-left">
              Дата
            </th>
            <th class="text-left">
              Прибыль, <v-icon>mdi-currency-rub</v-icon>
            </th>
            <th colspan="2" class="text-center">
              Абсолютный прирост, <v-icon>mdi-currency-rub</v-icon>
            </th>
            <th colspan="2" class="text-center">
              Темп роста, <v-icon>mdi-percent-outline</v-icon>
            </th>
            <th colspan="2" class="text-center">
              Темп прироста, <v-icon>mdi-percent-outline</v-icon>
            </th>
          </tr>
          <tr>
            <th></th>
            <th></th>
            <th class="text-center">
              Цепной
            </th>
            <th class="text-center">
              Базисный
            </th>
            <th class="text-center">
              Цепной
            </th>
            <th class="text-center">
              Базисный
            </th>
            <th class="text-center">
              Цепной
            </th>
            <th class="text-center">
              Базисный
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in data" :key="item.date">
            <td>{{ item.date }}</td>
            <td>{{ item.total }}</td>
            <td class="text-center">{{ item.abs_plus.chain_growth }}</td>
            <td class="text-center">{{ item.abs_plus.basis_growth }}</td>
            <td class="text-center">{{ item.growth_rate.chain_growth }}</td>
            <td class="text-center">{{ item.growth_rate.basis_growth }}</td>
            <td class="text-center">{{ item.increase_rate.chain_growth }}</td>
            <td class="text-center">{{ item.increase_rate.basis_growth }}</td>
          </tr>
        </tbody>
      </v-simple-table>
    </v-card-text>
  </v-card>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import 'vuetify/dist/vuetify.min.css'


  export default {
    name: "StatisticalDynamics",
    created() {
      apiClient
        .get('financialrecords/')
        .then(response => {
          this.rawData = response.data
          this.getData()
        })
    },
    data () {
      return {
        headers: [
        {
          text: 'Dessert',
          align: 'start',
          sortable: false,
          value: 'name',
          colspan: 2, // задаем свойство colspan равное 2
        },
        { text: 'Calories', value: 'calories', scope: 'col'},
        { text: 'Fat (g)', value: 'fat', scope: 'col' },
        { text: 'Carbs (g)', value: 'carbs' },
        { text: 'Protein (g)', value: 'protein' },
        { text: 'Iron (%)', value: 'iron' },
      ],
      desserts: [
        {
          name: 'Frozen Yogurt',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          iron: '1%',
        },
      ],
        rawData: null,
        data: [],
      }
    },
    methods: {
      financial(x) {
        return Number.parseFloat(x).toFixed(2);
      },
      getData() {
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
        let prev = null
        let first = result ? result[0] : null
        result.forEach(r => {
          this.data.push(
            {
              date: r.date,
              income: r.income,
              expenses: r.expenses,
              total: r.income-r.expenses,
              abs_plus: {
                chain_growth: prev ? (r.income-r.expenses) - (prev.income-prev.expenses) : '-',
                basis_growth: first ? (r.income-r.expenses) - (first.income-first.expenses) : '-'
              },
              growth_rate: { // Number.parseFloat(x).toFixed(2);
                chain_growth: prev ? this.financial((r.income-r.expenses) / (prev.income-prev.expenses) * 100) : '-',
                basis_growth: first ? this.financial((r.income-r.expenses) / (first.income-first.expenses) * 100) : '-'
              },
              increase_rate: {
                chain_growth: prev ? this.financial(((r.income-r.expenses) / (prev.income-prev.expenses) * 100)-100) : '-',
                basis_growth: first ? this.financial(((r.income-r.expenses) / (first.income-first.expenses) * 100)-100) : '-'
              }
            })
          prev = r
        })
      }
    }
  }
</script>

<style scoped>

</style>
