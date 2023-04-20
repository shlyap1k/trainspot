import colors from 'vuetify/es5/util/colors'

export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - trainspot',
    title: 'trainspot',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: '@/plugins/vue-mathjax.js', ssr: false }
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    '@nuxtjs/toast',
    'cookie-universal-nuxt'
  ],
auth: {
    strategies: {
        local: {
            endpoints: {
                login: {
                    url: '/api/login/',
                    method: 'post',
                    propertyName: 'access',
                    altProperty: 'refresh'
                },
                logout: {
                  url: '/api/logout/',
                  method: 'post',
                  propertyName: 'access',
                  altProperty: 'refresh'
                },
                user: false
            }
        }
    },
    redirect: {
        login: '/login'
    },
},
routes: [
  {
    path: '/pricelist',
    component: 'pages/pricelist.vue',
    meta: {
      public: true
    }
  }
],
router: {
    middleware: ['auth']
},
axios: {
    baseURL: 'http://localhost:8000',
    credentials: true,
    init(axios) {
      axios.defaults.withCredentials = true
    }
},
toast: {
    position: 'bottom-right',
    iconPack: 'fontawesome',
    duration: 3000,
    register: [
      {
        name: 'defaultSuccess',
        message: (payload) =>
          !payload.msg ? 'Операция успешно выполнена' : payload.msg,
        options: {
          type: 'success',
          icon: 'check'
        }
      },
      {
        name: 'defaultError',
        message: (payload) =>
          !payload.msg ? 'Ошибка' : payload.msg,
        options: {
          type: 'error',
          icon: 'times'
        }
      }
    ]
  },
  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  }
}
