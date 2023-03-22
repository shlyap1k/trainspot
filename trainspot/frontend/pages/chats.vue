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

                  <v-btn
                    variant="plain"
                    color="white"
                    rounded="xl"
                    theme="dark"
                  >
                    Создать чат
                  </v-btn>
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
              <messages-list :messages="getMessages()"/>
    <!--          {{chatId}}-->
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-card rounded="xl">
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
  import MessageBox from "@/components/chat/messages/MessageBox.vue";

  import { mapGetters } from 'vuex'
  export default {
    name: "chats",
    components: {
      'messages-list' : MessagesList,
      'message-box' : MessageBox
    },
    modules: [ChatList, MessagesList],
    mounted() {
      this.$store.dispatch("user/fetchChats")
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
        chatId: 'user/getChatId'
      })
    }
  }
</script>

<style scoped>

</style>
