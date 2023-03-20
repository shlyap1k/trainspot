<template>
  <v-card>
    <div v-for="chat in chats">
      <chat-element :chat="chat"/>
    </div>
  </v-card>
</template>

<script>
  import ChatElement from '@/components/chat/chat_list/ChatElement.vue'
  export default {
    name: "ChatList",
    modules: [ChatElement],
    props: {
      chats: {
        type: Array,
        required: true
      },
    }
  }
</script>

<style scoped>

</style>
