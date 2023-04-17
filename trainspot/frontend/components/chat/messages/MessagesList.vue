<template>
  <v-card>
    <v-card-title>
      Сообщения
    </v-card-title>
    <v-card-subtitle v-if="members">
      <members-list :members="members"/>
    </v-card-subtitle>
    <div v-if="messages">
      <v-card-text>
        <v-virtual-scroll
          :items="messages"
          :item-height="170"
          max-height="435"
        >
          <template v-slot="{ item }">
            <v-list-item
              :item-height="itemHeight(item)"
            >
              <message-block :message="item"/>
            </v-list-item>

          </template>
        </v-virtual-scroll>
      </v-card-text>
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
import MembersList from "@/components/chat/messages/MembersList.vue";

import {mapGetters} from "vuex";
// TODO добавить пользователя
  export default {
    name: "MessagesList",
    modules: [MessageBlock, MembersList],
    reactions: {},
    components: {
      'message-block' : MessageBlock,
      'members-list': MembersList
    },
    props: {
      messages: {
        type: Array,
        required: true
      },
      members: {
        type: Array,
        required: true
      },
    },
    methods: {
      itemHeight (item) {
        return 500
      }
    },
    computed: {
      ...mapGetters({
        chats: 'user/getChats',
        members: 'chat/getMembers'
      })
    }
  }
</script>

