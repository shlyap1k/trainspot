<template>
  <v-app>
    <v-col>
    <v-navigation-drawer
      v-model="drawer"
      :clipped="clipped"
      fixed
      app
    >
      <v-list  v-if="user">
        <v-list-item
          v-for="(item, i) in authenticatedItems"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-list v-else>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-icon>mdi-application</v-icon>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer />
    </v-app-bar>
    </v-col>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer
      :absolute="!fixed"
      app
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import { mapState } from 'vuex'
import 'vuetify/dist/vuetify.min.css'
export default {
  name: 'DefaultLayout',
  mounted() {
      this.$store.dispatch("user/fetchUser")
      // this.$store.dispatch("user/fetchSubscription", {userId: this.$store.state.user.data.id})
      this.$store.dispatch("user/fetchChats")
    },
  computed: {
    ...mapState('auth', ['loggedIn']),
    user() {
      return this.$store.state.user.data
    }
  },
  data () {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Главная',
          to: '/'
        },
        {
          icon: 'mdi-login',
          title: 'Войти',
          to: '/login'
        },
        {
          icon: 'mdi-clipboard-list',
          title: 'Список цен',
          to: '/pricelist'
        }
      ],
      authenticatedItems: [
        {
          icon: 'mdi-apps',
          title: 'Главная',
          to: '/'
        },
        {
          icon: 'mdi-clipboard-list',
          title: 'Список цен',
          to: '/pricelist'
        },
        {
          title: 'gyms',
          icon: 'mdi-dumbbell',
          to : '/gyms'
        },
        {
          title: 'Мои тренировки',
          icon: 'mdi-gymnastics',
          to : '/trainings'
        },
        {
          title: 'Профиль',
          icon: 'mdi-account',
          to: '/profile'
        },
        {
          title: 'Чаты',
          icon: 'mdi-forum',
          to: '/chats'
        },
        {
          title: 'Рассылки',
          icon: 'mdi-card-account-mail-outline',
          to: '/mailings'
        },
        {
          title: 'Статистика',
          icon: 'mdi-chart-bar',
          to: '/reports'
        },
        {
          title: 'Выход',
          icon: 'mdi-logout',
          to: '/logout'
        },
      ],
      title: 'TrainSpot',
    }
  }
}
</script>
