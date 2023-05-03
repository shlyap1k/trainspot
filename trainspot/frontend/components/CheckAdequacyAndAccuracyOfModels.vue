<template>
  <v-card>
    <v-card-title>
      Проверка адекватности и точности моделей
    </v-card-title>
    <v-card-text>
      <h3>
<!--        TODO: display json in human-readable form-->
        Проверка остаточной последовательности свойству случайности колебаний уровней ряда (с помощью критерия знаков)
      </h3>
      <p>
        Для показательной модели
      </p>
      <p>
        {{exponentialSignTestResult}}
      </p>
      <p>
        Для параболической модели
      </p>
      <p>
        {{quadraticSignTestResult}}
      </p>
      <p>
        Для линейной модели
      </p>
      <p>
        {{linearSignTestResult}}
      </p>
      <h3>
        Проверка соответствия распределения нормальному закону (с помощью коэффициентов асимметрии и эксцесса)
      </h3>
      <p>
        Для показательной модели
      </p>
      <p>
        {{exponentialNormTestResult}}
      </p>
      <p>
        Для параболической модели
      </p>
      <p>
        {{quadraticNormTestResult}}
      </p>
      <p>
        Для линейной модели
      </p>
      <p>
        {{linearNormTestResult}}
      </p>
      <h3>
        Тест Дарбина-Уотсона
      </h3>
      <p>
        Для показательной модели
      </p>
      <p>
        {{exponentialDWTestResult}}
      </p>
      <p>
        Для параболической модели
      </p>
      <p>
        {{quadraticDWTestResult}}
      </p>
      <p>
        Для линейной модели
      </p>
      <p>
        {{linearDWTestResult}}
      </p>
      <h3>
        Показатели точности модели (MAPE, S, SSE, MSE)
      </h3>
      <p>
        Для показательной модели
      </p>
      <p>
        {{exponentialAccuracyIndicators}}
      </p>
      <p>
        Для параболической модели
      </p>
      <p>
        {{quadraticAccuracyIndicators}}
      </p>
      <p>
        Для линейной модели
      </p>
      <p>
        {{linearAccuracyIndicators}}
      </p>
      <p>
        Лучшая модель: {{chooseBest( {linear: linearAccuracyIndicators, quadratic: quadraticAccuracyIndicators, exponential: exponentialAccuracyIndicators} )}}
      </p>
    </v-card-text>
  </v-card>
</template>

<script>
  import signTest from "@/src/statistics/statisticsTests/signTest";
  import normTest from "@/src/statistics/statisticsTests/normTest"
  import DurbinWatsonTest from "@/src/statistics/statisticsTests/DurbinWatsonTest";
  import calcAccuracyIndicators from "@/src/statistics/utils/AccuracyIndicators";
  import median_test from "@/src/statistics/statisticsTests/medianTest";
  import updown_test from "@/src/statistics/statisticsTests/updownTest";
  import chooseBestModel from "@/src/statistics/utils/getBestModel";
  export default {
    name: "CheckAdequacyAndAccuracyOfModels",
    props: {
      testResults: {
        type: Object,
        required: true
      },
      data: {
        type: Array,
        required: true
      }
    },
    // TODO: Сделать вывод о том, какая из моделей лучше описывает исходные данные
    // S - less is better
    // SSE - less is better
    // MSE - less is better
    // MAPE - less is better
    computed: {
      exponentialSignTestResult: function() {
        if (this.data) {
          return {
            medianTest: median_test(this.data.slice(1).map(row=>row[2])),
            updownTest: updown_test(this.data.slice(1).map(row=>row[2]))
          }
        }
        return null
      },
      quadraticSignTestResult: function() {
        if (this.data) {
          return {
            medianTest: median_test(this.data.slice(1).map(row=>row[2])),
            updownTest: updown_test(this.data.slice(1).map(row=>row[2]))
          }
        }
        return null
      },
      linearSignTestResult: function() {
        if (this.data) {
          return {
            medianTest: median_test(this.data.slice(1).map(row=>row[2])),
            updownTest: updown_test(this.data.slice(1).map(row=>row[2]))
          }
        }
        return null
      },
      exponentialNormTestResult: function() {
        if (this.data) {
          const exp = this.data.slice(1).map(r=>r[2])
          return normTest(exp)
        }
      },
      quadraticNormTestResult: function() {
        if (this.data) {
          const quad = this.data.slice(1).map(r=>r[3])
          return normTest(quad)
        }
      },
      linearNormTestResult: function() {
        if (this.data) {
          const lin = this.data.slice(1).map(r=>r[4])
          return normTest(lin)
        }
      },
      exponentialDWTestResult: function() {
        if (this.data) {
          const exp = this.data.slice(1).map(r=>r[2])
          return DurbinWatsonTest(exp)
        }
      },
      quadraticDWTestResult: function() {
        if (this.data) {
          const quad = this.data.slice(1).map(r=>r[3])
          return DurbinWatsonTest(quad)
        }
      },
      linearDWTestResult: function() {
        if (this.data) {
          const lin = this.data.slice(1).map(r=>r[4])
          return DurbinWatsonTest(lin)
        }
      },
      exponentialAccuracyIndicators: function() {
        if (this.data) {
          const exp = this.data.slice(1).map(r=>r[2])
          const realData = this.data.slice(1).map(r=>r[1])
          return calcAccuracyIndicators(realData, exp)
        }
      },
      quadraticAccuracyIndicators: function() {
        if (this.data) {
          const quad = this.data.slice(1).map(r=>r[3])
          const realData = this.data.slice(1).map(r=>r[1])
          return calcAccuracyIndicators(realData, quad)
        }
      },
      linearAccuracyIndicators: function() {
        if (this.data) {
          const lin = this.data.slice(1).map(r=>r[4])
          const realData = this.data.slice(1).map(r=>r[1])
          return calcAccuracyIndicators(realData, lin)
        }
      },
    },
    methods: {
      chooseBest(models) {
        return chooseBestModel(models)
      }
    }
  }
</script>

