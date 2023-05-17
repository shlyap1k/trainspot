<template>
  <v-card>
    <v-card-title>
      Карта пользователей
    </v-card-title>
    <v-card-text>
      <yandex-map
        ymap-class="map-box"
        :coords="[55.45, 37.36]"
        :controls="['fullscreenControl', 'searchControl', 'zoomControl']"
        :zoom="5"
      >
        <ymap-marker
          v-for="city in chartMapData"
          :coords="[
            city[1],
            city[2]
          ]"
          :marker-id="city[3]"
          :hint-content="`Количество пользователей: ${city[0]}`"
        />
      </yandex-map>
    </v-card-text>
  </v-card>
</template>

<script>
  import { yandexMap, ymapMarker } from 'vue-yandex-maps'
  export default {
    name: "UsersCountMap",
    components: {
      yandexMap,
      ymapMarker
    },
    props: {
      cities: {
        type: Array,
        required: true
      },
      users: {
        type: Array,
        required: true
      }
    },
    computed: {
      chartMapData: function() {
        const data = {}
        let index = 0
        this.cities.forEach(city => {
          data[city.name] = [0, city.lat, city.long, index]
          index += 1
          // data.push([city.name, 0, city.lat, city.long])
        })
        console.log(data)
        if (data) {
          this.users.forEach(user => {
            data[user.city][0] += 1
          })
        }
        return data
      }
    }
  }
</script>

<style lang="scss">
    .map-box {
        width: 100%;
        height: 600px;
    }
</style>
