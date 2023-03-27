<template>
  <v-row>
    <v-dialog
      v-model="dialog"
      persistent
      width="512"
      max-width="512px"
    >
      <template v-slot:activator="{ props }">
        <v-btn
          v-bind="props"
          icon
          @click="dialog=true"
        >
          <v-icon>mdi-account-plus</v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-row>
          <v-col cols="10">
            <v-card-title>
              <span class="text-h5">Регистрация</span>
            </v-card-title>
          </v-col>
          <v-spacer></v-spacer>
          <v-col>
            <v-btn
              color="blue-darken-1"
              icon
              @click="dialog = false"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="userData.username"
              label="Введите логин"
              counter
              required
            ></v-text-field>
            <v-text-field
              v-model="userData.email"
              label="Введите e-mail"
              counter
              required
            ></v-text-field>
            <v-text-field
              v-model="userData.first_name"
              label="Введите имя"
              counter
              required
            ></v-text-field>
            <v-text-field
              v-model="userData.last_name"
              label="Введите фамилию"
              counter
              required
            ></v-text-field>
            <v-text-field
              v-model="userData.password"
              label="Введите пароль"
              required
              :append-icon="
                userData.showPassword ? 'mdi-eye' : 'mdi-eye-off'
              "
              :type="userData.showPassword ? 'text' : 'password'"
              @click:append="
                userData.showPassword = !userData.showPassword
              "
            ></v-text-field>
            <v-text-field
              v-model="userData.password_confirm"
              label="Повторите пароль"
              :append-icon="
                userData.show_password_confirm ? 'mdi-eye' : 'mdi-eye-off'
              "
              :type="userData.show_password_confirm ? 'text' : 'password'"
              required
              @click:append="
                userData.show_password_confirm = !userData.show_password_confirm
              "
            ></v-text-field>
            <v-layout justify-space-between>
              <v-btn @click="signUp(userData)">
                Register
              </v-btn>
              <a href="">Forgot Password</a>
            </v-layout>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
  export default {
    name: "Register",
    data(){
      return {
        userData: {
          email: '',
          username: '',
          first_name: '',
          last_name: '',
          role: 'client',
          password: '',
          password_confirm: '',
          showPassword: false,
          show_password_confirm: false,
        },
        dialog: false
      }
    },
    methods: {
      async signUp(registrationInfo) {
        await this.$axios
          .$post('api/register/', registrationInfo)
          .then((response) => {
            console.log('Successful')
          })
          .catch((error) => {
            console.log('errors:', error.response)
          })
        registrationInfo.login = registrationInfo.username
        this.$auth.loginWith('local', {
          data: registrationInfo,
        })
      },
    },
  }
</script>
