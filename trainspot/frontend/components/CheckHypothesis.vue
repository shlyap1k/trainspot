<template>
  <v-card>
    <v-card-title>
      {{data.name}}
    </v-card-title>
    <v-card-text>
      <div v-if="data.median">
        Медиана: {{ data.median }}
      </div>
      <div v-if="data.series_count">
        Количество серий: {{ data.series_count }}
      </div>
      <div v-if="data.max_series_count">
        Самая длинная серия: {{ data.max_series_count }}
      </div>
      <div v-if="data.alpha">
        Уровень значимости: {{ data.alpha }}
      </div>
      <div v-if="data.ut">
        Квантиль нормального распределения уровня (1-alpha)/2: {{ data.ut }}
      </div>
      <div v-if="data.reject">
        Гипотеза об отсутствии тренда: принимается, динамика временного ряда не характеризуется наличием систематической составляющей - в изменениях отсутствует тенденция
      </div>
      <div v-else>
        Гипотеза об отсутствии тренда: отвергается, динамика временного ряда характеризуется наличием систематической составляющей - в изменениях присутствует тенденция
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
  export default {
    name: "CheckHypothesis",
    props: {
      data: {
        type: Object,
        required: true
      }
    }
  }
</script>
