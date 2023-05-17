import Vue from 'vue'
import YmapPlugin from 'vue-yandex-maps'

const settings = {
          apiKey: '23ba9a5b-30d8-46c3-8e41-cdf27e5c0384',
          lang: 'ru_RU',
          coordorder: 'latlong',
          enterprise: false,
          version: '2.1'
        } // настройки плагина

Vue.use(YmapPlugin, settings);
export default settings
