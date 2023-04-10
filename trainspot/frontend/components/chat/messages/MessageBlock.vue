<template>
  <v-card rounded="xl" max-width="400">
<!--     color="#EDE7F6"-->
    <v-card-title>
      <v-row>
        <v-col>
          <div class="text-subtitle-2">
            <p style="color: #bb5353">
              {{message.author.first_name + ' ' + message.author.last_name}}
            </p>
          </div>
        </v-col>
      </v-row>
    </v-card-title>
    <v-card-subtitle>
      <show-related-message
        v-if="parent"
        :message="message"
        :parent="parent"
      />
    </v-card-subtitle>
    <v-card-text>
      {{message.text}}
    </v-card-text>
    <v-card-actions>
      <reactions-block :message="message"/>
      <v-btn
        icon
        @click="reply_to(message.id)"
      >
        <v-icon>mdi-reply</v-icon>
      </v-btn>
    </v-card-actions>
    <v-spacer></v-spacer>
  </v-card>
</template>

<script>
  import { mapGetters } from 'vuex'
  import apiClient from '@/src/apiClient'
  export default {
    name: "MessageBlock",
    components: {
      ReactionsBlock: () => import('@/components/chat/messages/ReactionsBlock.vue'),
      ReactionsList: () => import('@/components/chat/messages/ReactionsList.vue'),
      ShowRelatedMessage: () => import('@/components/chat/messages/ShowRelatedMessage.vue'),
    },
    props: {
      message: {
        type: Object,
        required: true
      },
    },
    data() {
      return {
        parent: null
      }
    },
    created() {
      console.log("MESSASGE BLOCK CREATED")
      console.log(this.message.text)
      if (this.message.parent) {
        this.getParent(this.message.parent)
      }
    },
    methods: {
      reply_to(message_id) {
        console.log(this.message.parent)
        if (this.current_reply) {
          if (this.current_reply.id === message_id) {
            this.$store.dispatch('chat/unsetReply')
          } else {
            this.$store.dispatch('chat/replyToMessage', {message_id: message_id})
          }
        } else {
          this.$store.dispatch('chat/replyToMessage', {message_id: message_id})
        }
      },
      getParent(parent_id) {
        this.parent = this.messages.filter(message => {
          return parent_id === message.id
        })[0]
      }
    },
    computed: {
      ...mapGetters({
        current_reply: 'chat/getAnswerTo',
        messages: 'chat/getMessages'
      })
    }
  }
</script>

<style scoped>
  .message-block-style >>> .v-card {
    color: #EDE7F6
  }
</style>
