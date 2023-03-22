<template>
  <v-card>
    <v-card-title>Сообщения</v-card-title>
    <div v-if="messages">
      <v-virtual-scroll
        :items="messages"
        :item-height="170"
        max-height="470"
      >
        <template v-slot="{ item }">
          <v-list-item
            :item-height="itemHeight(item)"
          >
            <message-block :message="item"/>
          </v-list-item>

        </template>
      </v-virtual-scroll>
    </div>
    <div v-else>
      <v-card-text>
        Нет сообщений
      </v-card-text>
    </div>
  </v-card>

</template>

<script>
import MessageBlock from "@/components/chat/messages/MessageBlock.vue";
import apiClient from "@/src/apiClient";
  export default {
    name: "MessagesList",
    modules: [MessageBlock],
    reactions: {},
    components: {
      'message-block' : MessageBlock,
    },
    props: {
      messages: {
        type: Array,
        required: true
      },
    },
    methods: {
      getReactions(message) {
        this.reactions = apiClient.get("messagereactions/")
      },
      itemHeight (item) {
        return 500
      }
    }
  }
</script>

