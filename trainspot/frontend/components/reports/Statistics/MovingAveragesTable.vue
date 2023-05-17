<template>
  <div>
    <h2>{{tableName}}</h2>
    <v-simple-table>
      <thead>
        <tr>
          <th class="text-left">
            Дата
          </th>
          <th class="text-left">
            {{ valueType }}
          </th>
          <th colspan="2" class="text-center">
            Скользящие средние
          </th>
          <th rowspan="2" class="text-center">
            Взвешенная скользящая средняя, l=5
          </th>
        </tr>
        <tr>
          <th></th>
          <th></th>
          <th class="text-center">
            l=3
          </th>
          <th class="text-center">
            l=7
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in skipFirst(data)" :key="item.date">
          <td>{{ item[0] }}</td>
          <td>{{ item[1] }}</td>
          <td class="text-center" v-if="item[2]">{{ item[2].toFixed(2) }}</td>
          <td class="text-center" v-else>-</td>
          <td class="text-center" v-if="item[4]">{{ item[4].toFixed(2) }}</td>
          <td class="text-center" v-else>-</td>
          <td class="text-center" v-if="item[3]">{{ item[3].toFixed(2) }}</td>
          <td class="text-center" v-else>-</td>
        </tr>
      </tbody>
    </v-simple-table>
  </div>
</template>

<script>
  export default {
    name: "MovingAveragesTable",
    props: {
      valueType: String,
      tableName: String,
      data: Array
    },
    methods: {
      skipFirst(arr) {
        return arr.slice(1)
      }
    }
  }
</script>

