<template>
  <v-card rounded="xl">
<!--    <div v-for="chat in chats">-->

    <v-virtual-scroll
      :items="chats"
      :item-height="120"
      height="600"
    >
      <template v-slot="{ item }">
        <v-list-item>
<!--          <chat-element :chat="chat"/>-->
          <v-list-item-content>
            <chat-element :chat="item"/>
            <v-divider></v-divider>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-virtual-scroll>
<!--    </div>-->
  </v-card>
</template>

<script>
  import ChatElement from '@/components/chat/chat_list/ChatElement.vue'
  export default {
    // TODO создать чат
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
