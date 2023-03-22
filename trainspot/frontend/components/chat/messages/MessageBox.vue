<template>
  <v-card>
    <v-card-actions>
      <v-form v-on:submit="sendMessage">
        <div class="d-flex align-center justify-space-between">
          <v-textarea
            label="Ваше сообщение"
            rows="1"
            class="mx-6 ml-5"
            v-model="textMessage"
            style="width:400px;"
          ></v-textarea>
          <v-btn
            variant="plain"
            rounded="xl"
            theme="dark"
            icon
            @click="sendMessage"
          >
            <v-icon>mdi-send</v-icon>
          </v-btn>
        </div>
      </v-form>
    </v-card-actions>
  </v-card>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import axios from "axios";

  export default {
    name: "MessageBox",
    props: {
      chat: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        textMessage: null,
        parent: null
      }
    },
    methods: {
      sendMessage() {
        if (this.textMessage) {
          const data = new FormData()
          data.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
          data.append("text", this.textMessage)
          data.append("chat", this.chat)
          data.append("author", this.$store.state.user.data.id)
          if (this.parent) {
            data.append("parent", this.parent)
          }
          axios({
              method: 'post',
              url: 'http://localhost:8000/api/messages/',
              data: data,
              withCredentials: true,
              header: {
                'Accept': 'application/json',
                'Content-Type': 'multipart/form-data',
              },
            })
          // apiClient.post('messages/', data)
          this.textMessage = ''
        }
      }
    }
  }
</script>

<style scoped>

</style>
