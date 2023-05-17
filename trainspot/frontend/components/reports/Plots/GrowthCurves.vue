<template>
  <v-card>
    <v-card-title>
      Кривые роста
    </v-card-title>
    <v-card-text>

      Уравнение линейной модели:
      <katex-element :expression="formulaLinear"/><br/>
      Уравнение параболической модели:
      <katex-element :expression="formulaQuadratic"/><br/>
      Уравнение показательной модели:
      <katex-element :expression="formulaExpo"/><br/>

      <GChart type="LineChart" :data="series" :options="optionsLinear" />
      <check-adequacy-and-accuracy-of-models :data="series" :test-results="testResults" v-if="testResults"/>
      <h2>Расчет параметров линейной, параболической и показательной модели</h2>
      <models-param-table :data="data"/>

    </v-card-text>
  </v-card>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  import exponentialRegression from "@/src/statistics/regressionModels/exponentialRegression";
  import linearRegression from "@/src/statistics/regressionModels/linearRegression";
  import quadraticRegression from "@/src/statistics/regressionModels/quadraticRegression";
  import ModelsParamTable from "@/components/reports/Statistics/ModelsParamTable.vue";
  import CheckAdequacyAndAccuracyOfModels from "@/components/reports/Statistics/CheckAdequacyAndAccuracyOfModels.vue";
  export default {
    name: "GrowthCurves",
    components: {
      GChart,
      ModelsParamTable,
      CheckAdequacyAndAccuracyOfModels
    },
    props: {
      data: {
        type: Array,
        required: true
      },
      testResults: {
        type: Object,
        required: true
      },
      actionName: String
    },
    data () {
      return {
        formulaLinear: "c = \\pm\\sqrt{a^2 + b^2}",
        formulaQuadratic: "'x = {-b \pm \sqrt{b^2-4ac} \over 2a}.'",
        formulaExpo: "'x = {-b \pm \sqrt{b^2-4ac} \over 2a}.'",
        actual: [],
        optionsLinear: {
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        optionsQuadratic: {
          title: 'Параболическая модель',
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        optionsExpo: {
          title: 'Показательная модель',
          curveType: 'function',
          legend: {position: 'bottom'},
          height: 500
        },
        linearParams: {},
        quadraticParams: {},
        exponentialParams: {},
      }
    },
    computed: {
      exponentialSeries: function() {
        if (this.data.length > 1) {
          // console.log(this.data.length)
          return this.calcExponential()
        }
        return [['Дата', this.actionName ? this.actionName : 'Количество']]
      },
      quadraticSeries: function() {
        if (this.data.length > 1) {
          return this.calcQuadratic()
        }
        return [['Дата', this.actionName ? this.actionName : 'Количество']]
      },
      linearSeries: function() {
        if (this.data.length > 1) {
          return this.calcLinear()
        }
        return [['Дата', this.actionName ? this.actionName : 'Количество']]
      },
      series: function() {
        const series = [['Дата', 'Фактические данные', 'Показательная модель', 'Параболическая модель', 'Линейная модель']]
        if (this.data.length > 1) {
          for (let i = 1; i < this.exponentialSeries.length-1; i++) {
            series.push([this.exponentialSeries[i][0], this.data[i][1], this.exponentialSeries[i][1],
              this.quadraticSeries[i][1], this.linearSeries[i][1]])
          }
        }
        return series
      }
    },
    methods: {
      calcExponential() {
        // Вычисление параметров показательной регрессии
        this.exponentialParams = exponentialRegression(this.data);
        const a = this.exponentialParams.a;
        const b = this.exponentialParams.b;
        // {{ exponentialParams.a }} * e ^ {{ exponentialParams.b }} * x
        // "c = \\pm\\sqrt{a^2 + b^2}"
        this.formulaExpo = "y = " + a.toFixed(2) + " \\cdot e^{" + b.toFixed(2) + " \\cdot x}"
        // Построение кривой роста
        // console.log(this.data)
        const exponentialSeries = [['Дата', this.actionName ? this.actionName : 'Количество']]
        for (let i = 0; i <= this.data.length-1; i++) {
          const y = a * Math.exp(b * (i-(this.data.length/2)));

          exponentialSeries.push([this.data[i][0], y/10000]);
        }
        return exponentialSeries
      },
      calcQuadratic() {
        // Вычисление параметров параболической регрессии
        this.quadraticParams = quadraticRegression(this.data);
        const a = this.quadraticParams.a;
        const b = this.quadraticParams.b;
        const c = this.quadraticParams.c;

        this.formulaQuadratic = "y = " + a.toFixed(2) + " + " + b.toFixed(2) + " \\cdot x + " + c.toFixed(2) + " \\cdot x^2"

        // Построение кривой роста
        const quadraticSeries = [['Дата', this.actionName ? this.actionName : 'Количество']]
        for (let i = 0; i <= this.data.length-1; i++) {
          const y = a + b * (i-(this.data.length/2)) + c * (i-(this.data.length/2)) * (i-(this.data.length/2));
          quadraticSeries.push([this.data[i][0], y/10]);
        }
        return quadraticSeries
      },
      calcLinear() {
        // Вычисление параметров линейной регрессии
        this.linearParams = linearRegression(this.data);
        const a = this.linearParams.a;
        const b = this.linearParams.b;
        this.formulaLinear = "y = " + a.toFixed(2) + " + " + b.toFixed(2) + " \\cdot x"
        // Построение кривой роста
        const linearSeries = [['Дата', this.actionName ? this.actionName : 'Количество']]
        for (let i = 0; i <= this.data.length-1; i++) {
          const y = a + b * (i-(this.data.length/2));
          linearSeries.push([this.data[i][0], y]);
        }
        return linearSeries
      }
    }
  }
</script>
