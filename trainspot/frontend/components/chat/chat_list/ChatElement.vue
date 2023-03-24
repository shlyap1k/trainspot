<template>
<v-card @click="selectChat(chat.id)">
  <v-card-title>{{chat.name}}</v-card-title>
  <v-card-subtitle>{{chat.creator.first_name + ' ' + chat.creator.last_name + ' (@' + chat.creator.username}})</v-card-subtitle>
  <v-card-text>{{ lastMessage(chat.messages).substring(0,30)+".."}}</v-card-text>
</v-card>
</template>

<script>
  import {mapGetters} from "vuex";

  export default {
    name: "ChatElement",
    props: {
      chat: {
        type: Object,
        required: true
      },
    },
    methods: {
      lastMessage(messages) {
        if (messages.slice(-1).pop()) {
          let author = messages.slice(-1).pop().author
          return author.first_name + ' ' + author.last_name + ': ' + messages.slice(-1).pop().text
        } else {
          return 'Нет сообщений'
        }
      },
      selectChat(chatId) {
        this.$store.dispatch("user/selectCurrentChat", {chatId: chatId})
        this.$store.dispatch("chat/fetchMessages", {chat: chatId})
      },
    }
  }
</script>

<style scoped>

</style>
