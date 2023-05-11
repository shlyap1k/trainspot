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
<!--        {{exponentialSignTestResult}}-->
        <check-hypothesis :data="exponentialSignTestResult['medianTest']" v-if="exponentialSignTestResult['medianTest']"/>
        <check-hypothesis :data="exponentialSignTestResult['updownTest']" v-if="exponentialSignTestResult['updownTest']"/>
      </p>
      <p>
        Для параболической модели
      </p>
      <p>
<!--        {{quadraticSignTestResult}}-->
<!--        <check-hypothesis :data="quadraticSignTestResult" v-if="quadraticSignTestResult"/>-->
        <check-hypothesis :data="quadraticSignTestResult['medianTest']" v-if="quadraticSignTestResult['medianTest']"/>
        <check-hypothesis :data="quadraticSignTestResult['updownTest']" v-if="quadraticSignTestResult['updownTest']"/>
      </p>
      <p>
        Для линейной модели
      </p>
      <p>
<!--        {{linearSignTestResult}}-->
        <check-hypothesis :data="linearSignTestResult['medianTest']" v-if="linearSignTestResult['medianTest']"/>
        <check-hypothesis :data="linearSignTestResult['updownTest']" v-if="linearSignTestResult['updownTest']"/>
      </p>
      <h3>
        Проверка соответствия распределения нормальному закону (с помощью коэффициентов асимметрии и эксцесса)
      </h3>
      <p>
        Для показательной модели
      </p>
      <p>
        Коэффициент ассиметрии: {{exponentialNormTestResult.skewness.toFixed(2)}}
        Коэффициент эксцесса: {{exponentialNormTestResult.kurtosis.toFixed(2)}}
      </p>
      <p v-if="exponentialNormTestResult.kurtosis.isNormal">
        Распределение соответствует нормальному распределению
      </p>
      <p v-else>
        Распределение не соответствует нормальному распределению
      </p>
      <p>
        Для параболической модели
      </p>
      <p>
        Коэффициент ассиметрии: {{quadraticNormTestResult.skewness.toFixed(2)}}
        Коэффициент эксцесса: {{quadraticNormTestResult.kurtosis.toFixed(2)}}
      </p>
      <p v-if="quadraticNormTestResult.kurtosis.isNormal">
        Распределение соответствует нормальному распределению
      </p>
      <p v-else>
        Распределение не соответствует нормальному распределению
      </p>
      <p>
        Для линейной модели
      </p>
      <p>
        Коэффициент ассиметрии: {{linearNormTestResult.skewness.toFixed(2)}}
        Коэффициент эксцесса: {{linearNormTestResult.kurtosis.toFixed(2)}}
      </p>
      <p v-if="linearNormTestResult.kurtosis.isNormal">
        Распределение соответствует нормальному распределению
      </p>
      <p v-else>
        Распределение не соответствует нормальному распределению
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
      <v-simple-table>
        <thead>
          <th class="text-left">
            Модель
          </th>
          <th class="text-left">
            MAPE
          </th>
          <th class="text-left">
            S
          </th>
          <th class="text-left">
            SSE
          </th>
          <th class="text-left">
            MSE
          </th>
        </thead>
        <tbody>
          <tr>
            <td>
              Показательная
            </td>
            <td>
              {{ exponentialAccuracyIndicators.MAPE.toFixed(2) }}%
            </td>
            <td>
              {{exponentialAccuracyIndicators.S.toFixed(2)}}
            </td>
            <td>
              {{exponentialAccuracyIndicators.SSE.toFixed(2)}}
            </td>
            <td>
              {{exponentialAccuracyIndicators.MSE.toFixed(2)}}
            </td>
          </tr>
        <tr>
            <td>
              Параболическая
            </td>
            <td>
              {{ quadraticAccuracyIndicators.MAPE.toFixed(2) }}%
            </td>
            <td>
              {{quadraticAccuracyIndicators.S.toFixed(2)}}
            </td>
            <td>
              {{quadraticAccuracyIndicators.SSE.toFixed(2)}}
            </td>
            <td>
              {{quadraticAccuracyIndicators.MSE.toFixed(2)}}
            </td>
          </tr>
        <tr>
            <td>
              Линейная
            </td>
            <td>
              {{ linearAccuracyIndicators.MAPE.toFixed(2) }}%
            </td>
            <td>
              {{linearAccuracyIndicators.S.toFixed(2)}}
            </td>
            <td>
              {{linearAccuracyIndicators.SSE.toFixed(2)}}
            </td>
            <td>
              {{linearAccuracyIndicators.MSE.toFixed(2)}}
            </td>
          </tr>
        </tbody>
      </v-simple-table>
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
  import checkHypothesis from "@/components/CheckHypothesis.vue";
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
            medianTest: median_test(this.data.slice(1).map(row=>row[3])),
            updownTest: updown_test(this.data.slice(1).map(row=>row[3]))
          }
        }
        return null
      },
      linearSignTestResult: function() {
        if (this.data) {
          return {
            medianTest: median_test(this.data.slice(1).map(row=>row[4])),
            updownTest: updown_test(this.data.slice(1).map(row=>row[4]))
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
      }, // MAPE, S, SSE, MSE
      exponentialAccuracyIndicators: function() {
        if (this.data) {
          const exp = this.data.slice(1).map(r=>r[2])
          const realData = this.data.slice(1).map(r=>r[1])
          const result = calcAccuracyIndicators(realData, exp)

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

