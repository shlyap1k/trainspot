<template>
  <div>
    <v-row>
      <v-col cols="4">
        <v-row>
          <v-col>
            <v-card
              rounded="xl"
              class="mx-auto"
              v-if="chats"
            >
              <div class="d-flex align-center justify-space-between">
                <v-card-title>
                  Ваши чаты

                </v-card-title>

                  <create-chat-form/>
              </div>
              <chat-list :chats="chats"/>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col>

          </v-col>
        </v-row>
      </v-col>

      <v-col cols="6">
        <v-row>
          <v-col>
            <v-card rounded="xl">
              <messages-list :messages="messages" :members="chat"/>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-card rounded="xl" v-if="this.chatId">
              <message-box :chat="this.chatId"/>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  import ChatList from '@/components/chat/chat_list/ChatList.vue'
  import MessagesList from '@/components/chat/messages/MessagesList.vue'
  import MessageBox from "@/components/chat/messages/messages_forms/MessageBox.vue";
  import CreateChatForm from "@/components/chat/chat_list/Forms/CreateChatForm.vue";

  import { mapGetters } from 'vuex'
  export default {
    name: "chats",
    components: {
      MessagesList,
      MessageBox,
      CreateChatForm
    },
    modules: [ChatList, MessagesList],
    mounted() {
      this.$store.dispatch("user/fetchChats")
      this.$store.dispatch("chat/fetchMessages", {chat: this.$store.state.user.chatId})
    },
    methods: {
      getMessages() {
        if (this.chats) {
          if (this.chats[this.chatId]) {
            return this.chats[this.chatId - 1].messages
          }
        }
      }
    },
    computed: {
      ...mapGetters({
        chats: 'user/getChats',
        chatId: 'user/getChatId',
        messages: 'chat/getMessages',
      })
    }
  }
</script>

<style scoped>

</style>
