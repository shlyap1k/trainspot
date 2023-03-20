<template>
  <form @submit.prevent="login">
    <div>
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username">
    </div>
    <div>
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password">
    </div>
    <button type="submit">Login</button>
  </form>
</template>

<script>
  import apiClient from '~/src/apiClient'
  export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login () {
      apiClient.dispatch('login', {
        username: this.username,
        password: this.password
      })
      // apiClient.get('gyms/').then(response => {
      //   this.gyms = response.data.results
      // })
    }
  }
}
</script>
