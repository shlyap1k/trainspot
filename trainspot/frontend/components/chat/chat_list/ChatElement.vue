<template>
<v-card @click="selectChat(chat.id)">
  <v-card-title>{{chat.name}}</v-card-title>
  <v-card-subtitle>{{chat.creator.first_name + ' ' + chat.creator.last_name + ' (@' + chat.creator.username}})</v-card-subtitle>
  <v-card-text>{{ lastMessage(chat.messages)}}</v-card-text>
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
          return messages.slice(-1).pop().text
        }
      },
      selectChat(chatId) {
        this.$store.dispatch("user/selectCurrentChat", {chatId: chatId})
      },
    }
  }
</script>

<style scoped>

</style>
