<template>
  <v-card>
    <v-card-subtitle v-if="reply_to">
<!--      {{getMessage(reply_to)}}-->
      <v-row>
        <v-col>
      Вы отвечаете на сообщение от {{reply_to.author.first_name + ' ' + reply_to.author.last_name + ': ' + reply_to.text.substring(0,30)+".."}}
          <v-divider></v-divider>
        </v-col>
        <v-col>
          <v-btn
            @click="unsetReply"
            icon>
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-card-actions>
      <v-form v-on:submit="sendMessage">
        <div class="d-flex align-center justify-space-between">
          <v-textarea
            label="Ваше сообщение"
            rows="1"
            class="mx-6 ml-5"
            v-model="textMessage"
            style="width:400px;"
            rounded="xl"
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
  import {mapGetters} from "vuex";

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
          if (this.reply_to) {
            data.append("parent", this.reply_to.id)
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
          this.textMessage = '' // TODO добавить сообщение после отправки
          this.$store.dispatch('chat/fetchMessages', {chat: this.$store.state.user.chatId})
          this.$store.dispatch('user/fetchChats')
          this.$store.dispatch('chat/unsetReply')
        }
      },
      getMessage(message_id) {
        apiClient
          .get('messages/'+message_id+'/')
          .then(response => {
            this.parent = response.data
          })
        console.log(this.parent)
      },
      unsetReply() {
        this.$store.dispatch('chat/unsetReply')
      }
    },
    computed: {
      ...mapGetters({
        reply_to: 'chat/getAnswerTo'
      })
    }
  }
</script>

<style scoped>

</style>
