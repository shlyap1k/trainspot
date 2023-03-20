<template>
   <v-app >
      <v-main>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex xs12 sm8 md4>
                  <v-card class="elevation-12">
                     <v-toolbar dark color="primary">
                        <v-toolbar-title>Вход</v-toolbar-title>
                     </v-toolbar>
                     <v-card-text>
                     <form ref="form" @submit.prevent="logInUser(userData)">
                            <v-text-field
                              v-model="userData.login"
                              name="username"
                              label="логин"
                              type="text"
                              placeholder="username"
                              required
                           ></v-text-field>

                            <v-text-field
                              v-model="userData.password"
                              name="password"
                              label="пароль"
                              type="password"
                              placeholder="password"
                              :append-icon="
                                userData.showPassword ? 'mdi-eye-off' : 'mdi-eye'
                              "
                              :type="userData.showPassword ? 'text' : 'password'"
                              required
                           ></v-text-field>
                           <v-btn type="submit" class="mt-4" color="primary" value="log in">войти</v-btn>
                      </form>
                     </v-card-text>
                  </v-card>

               </v-flex>
            </v-layout>
         </v-container>
      </v-main>
   </v-app>
</template>

<script>
export default {
  name: "Login",
  data: () => ({
    userData: { login: '', password: '', showPassword: false },
  }),
  methods: {
    async logInUser(userData) {
      try {
        await this.$auth.loginWith('local', {
          data: userData,
        })
        // this.$store.commit('setUser', this.$axios.get('/api/profile/'))
        this.$store.dispatch('user/fetchUser');
        this.$toast.success('Успешный вход')
      } catch (error) {
        this.$toast.error('Ошибка')
      }
    },
  },
};
</script>
