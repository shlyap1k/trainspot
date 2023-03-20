<template>
  <div>
    <v-row>
      <v-col cols="4">
        <v-card

          class="mx-auto"
          v-if="chats"
        >
          <v-card-title>Ваши чаты</v-card-title>
          <chat-list :chats="chats"/>
          <v-btn
            variant="outlined"
            size="large"
            icon
            color="info"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-card>
      </v-col>
      <v-col cols="6">
        <v-card>
          <v-card-title>a</v-card-title>
          <messages-list :messages="getMessages()"/>
<!--          {{chatId}}-->
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  import ChatList from '@/components/chat/chat_list/ChatList.vue'
  import MessagesList from '@/components/chat/messages/MessagesList.vue'

  import { mapGetters } from 'vuex'
  export default {
    name: "chats",
    components: {
      'messages-list' : MessagesList,
    },
    modules: [ChatList, MessagesList],
    mounted() {
      this.$store.dispatch("user/fetchChats")
    },
    methods: {
      getMessages() {
        if (this.chats[this.chatId]) {
          return this.chats[this.chatId-1].messages
        }
      }
    },
    computed: {
      ...mapGetters({
        chats: 'user/getChats',
        chatId: 'user/getChatId'
      })
    }
  }
</script>

<style scoped>

</style>
