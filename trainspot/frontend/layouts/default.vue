<!--<template>-->
<!--  <div>-->
<!--    <nav-->
<!--      class="navbar header has-shadow is-primary"-->
<!--      role="navigation"-->
<!--      aria-label="main navigation"-->
<!--    >-->
<!--      <div class="navbar-brand">-->
<!--        <a class="navbar-item" href="/">-->
<!--&lt;!&ndash;          <img src="~assets/buefy.png" alt="Buefy" height="28" />&ndash;&gt;-->
<!--        </a>-->

<!--        <div class="navbar-burger">-->
<!--          <span />-->
<!--          <span />-->
<!--          <span />-->
<!--        </div>-->
<!--      </div>-->
<!--    </nav>-->

<!--    <section class="main-content columns">-->
<!--      <aside class="column is-2 section">-->
<!--        <p class="menu-label is-hidden-touch">General</p>-->
<!--        <ul class="menu-list">-->
<!--          <li v-for="(item, key) of globalItems" :key="key">-->
<!--            <nuxt-link :to="item.to" exact-active-class="is-active">-->
<!--              <v-icon :icon="item.icon" />-->
<!--              {{ item.title }}-->
<!--            </nuxt-link>-->
<!--          </li>-->
<!--          <span v-if="loggedIn">-->
<!--            <li v-for="(item, key) of authenticatedItems" :key="key">-->
<!--              <nuxt-link :to="item.to" exact-active-class="is-active">-->
<!--                <v-icon :icon="item.icon" />-->
<!--                {{ item.title }}-->
<!--              </nuxt-link>-->
<!--            </li>-->
<!--          </span>-->
<!--        </ul>-->
<!--      </aside>-->

<!--      <div class="container column is-10">-->
<!--        <nuxt />-->
<!--      </div>-->
<!--    </section>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import { mapState } from 'vuex'-->
<!--export default {-->
<!--  data() {-->
<!--    return {-->
<!--      globalItems: [-->
<!--        {-->
<!--          title: 'Home',-->
<!--          icon: 'home',-->
<!--          to: { name: 'index' }-->
<!--        }-->
<!--      ],-->
<!--      authenticatedItems: [-->
<!--        {-->
<!--          title: 'Выход',-->
<!--          icon: 'logout',-->
<!--          to: { name: 'logout' }-->
<!--        },-->
<!--        {-->
<!--          title: 'вы авторизованы',-->
<!--          icon: 'test',-->
<!--          to: {name:'/gyms'}-->
<!--        },-->
<!--        {-->
<!--          title: 'todos',-->
<!--          icon: 'home',-->
<!--          to : { name: 'todos'}-->
<!--        },-->
<!--        {-->
<!--          title: 'fruits',-->
<!--          icon: 'home',-->
<!--          to : { name: 'fruits'}-->
<!--        },-->
<!--        {-->
<!--          title: 'gyms',-->
<!--          icon: 'home',-->
<!--          to : { name: 'gyms'}-->
<!--        }-->
<!--      ]-->
<!--    }-->
<!--  },-->
<!--  computed: {-->
<!--    ...mapState('auth', ['loggedIn'])-->
<!--  }-->
<!--}-->
<!--</script>-->

<template>
  <v-app dark>
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
      <v-btn
        icon
        @click.stop="clipped = !clipped"
      >
        <v-icon>mdi-application</v-icon>
      </v-btn>
      <v-btn
        icon
        @click.stop="fixed = !fixed"
      >
        <v-icon>mdi-minus</v-icon>
      </v-btn>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer />
    </v-app-bar>
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
export default {
  name: 'DefaultLayout',
  mounted() {
      this.$store.dispatch("user/fetchUser")
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
      ],
      authenticatedItems: [
        {
          icon: 'mdi-apps',
          title: 'Главная',
          to: '/'
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
          to: '/profile'
        },
        {
          title: 'Рассылки',
          icon: 'mdi-card-account-mail-outline',
          to: '/mailings'
        },
        {
          title: 'Отчёты',
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
