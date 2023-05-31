<template>
  <div class="login-page">
    <v-container>
      <v-layout flex align-center justify-center>
        <v-flex>
          <v-card>
            <div class="d-flex align-center justify-space-between">
            <v-card-title flex align-center justify-center>
              <h1>Авторизация</h1>
            </v-card-title>
            <register/>
            </div>
            <v-card-text class="pt-4">
              <div>
                <v-form ref="form">
                  <v-text-field
                    v-model="userData.login"
                    label="Введите ваш логин"
                    counter
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="userData.password"
                    label="Введите ваш пароль"
                    required
                    :append-icon="
                      userData.showPassword ? 'mdi-eye' : 'mdi-eye-off'
                    "
                    :type="userData.showPassword ? 'text' : 'password'"
                    @click:append="
                      userData.showPassword = !userData.showPassword
                    "
                  ></v-text-field>
                  <v-layout justify-space-between>
                    <v-btn @click="logInUser(userData)">
                      Войти
                    </v-btn>
                  </v-layout>
                </v-form>
              </div>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
  import Register from "@/components/Register.vue";
export default {
  name: "Login",
  components: {
    Register
  },
  data: () => ({
    userData: { login: '', password: '', showPassword: false },
  }),
  methods: {
    async logInUser(userData) {
      try {
        await this.$auth.loginWith('local', {
          data: userData,
        })
        this.$store.dispatch('user/fetchUser');
        this.$toast.success('Успешный вход')
      } catch (error) {
        this.$toast.error('Ошибка')
      }
    },
  },
};
</script>
