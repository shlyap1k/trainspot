<template>
  <v-layout flex align-center justify-center>
    <v-flex xs8 sm8 elevation-8>
      <v-card>
        <v-card-title v-if="role=='client'">
          Написать обращение к организации
        </v-card-title>
        <v-card-title v-if="role=='admin'">
          Написать обращение к пользователю
        </v-card-title>
        <v-sheet class="mx-auto">
          <v-form @submit.prevent>
            <v-card-text>

              <v-select
                v-model="selectedUser"
                :items="users"
                item-text="username"
                attach
                label="Найти пользователя"
                return-object
              >
                <template v-slot:prepend-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-text-field
                        v-model="searchTerm"
                        placeholder="Введите логин пользователя"
                        @input="searchUsers"
                      >
                      </v-text-field>
                    </v-list-item-content>
                  </v-list-item>
                  <v-divider
                    class="mt-2"
                  >
                  </v-divider>
                </template>
              </v-select>

              <v-text-field
                v-model="subject"
                label="Тема обращения"
              >

              </v-text-field>
              <v-textarea
                v-model="appealText"
                :rules="rules"
                label="Текст обращения"
              ></v-textarea>
            </v-card-text>
            <v-card-actions>
              <v-btn type="submit" block class="mt-2" @click="submit">Отправить</v-btn>
            </v-card-actions>
          </v-form>
        </v-sheet>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import axios from "axios";

  export default {
    name: "AppealForm",
    props: {
      user: {
        type: Object,
        required: true
      }
    },
    data: () => ({
      searchTerm: null,
      users: [],
      usersCopy: [],
      appealText: '',
      subject: '',
      selectedUser: null,
      role: 'client',
      rules: [
        value => {
          if (value) return true
          return 'Нужно ввести текст.'
        },
      ],
    }),
    created() {
      this.role = this.$store.state.user.data.role
    },
    mounted() {
      if (this.role === 'admin') {
        apiClient
          .get('users/')
          .then((response) => {
            console.log(response.data)
            this.users = response.data.results.map(user => {
              return user
            })
          })
        this.usersCopy = [...this.users];
      }
    },
    methods: {
      submit() {
        const data = new FormData();
        data.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
        data.append("content", this.appealText)
        data.append("subject", this.subject)
        data.append("from_user", this.$store.state.user.data.id)
        if (this.selectedUser) {
          data.append("to_user", this.selectedUser.id)
        } else {
          data.append("to_user", 1)
        }
        axios({
            method: 'post',
            url: 'http://localhost:8000/api/newsletters/',
            data: data,
            withCredentials: true,
            header: {
              'Accept': 'application/json',
              'Content-Type': 'multipart/form-data',
            },
          })

        this.appealText = ''
        this.subject = ''
        this.selectedUser = null
      },
      searchUsers (e) {
        this.usersCopy = [...this.users];
        if (!this.searchTerm) {
          this.users = this.usersCopy;
          apiClient
          .get('users/')
          .then((response) => {
            this.users = response.data.results.map(user => {
              return user
            })
          })
        }
        this.users = this.usersCopy.filter(user => {
          return user.username.toLowerCase().indexOf(this.searchTerm.toLowerCase()) > -1
        })
      },
    }
  }
</script>
