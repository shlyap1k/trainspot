<template>
  <v-layout flex align-center justify-center>
    <v-flex xs8 sm8 elevation-8>
      <v-card>
        <v-card-title>
          Написать обращение к организации
        </v-card-title>
        <v-sheet class="mx-auto">
          <v-form @submit.prevent>
            <v-card-text>
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
      appealText: '',
      subject: '',
      rules: [
        value => {
          if (value) return true

          return 'Нужно ввести текст.'
        },
      ],
    }),
    methods: {
      submit() {
        const data = new FormData();
        data.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
        data.append("content", this.appealText)
        data.append("subject", this.subject)
        data.append("from_user", this.$store.state.user.data.id)
        data.append("to_user", 1)
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
      }
    }
  }
</script>
