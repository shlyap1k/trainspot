<template>
  <div :style="{ backgroundColor }">
    <v-row>

      <v-col cols="3">
        <v-btn
          variant="outlined"
          size="large"
          icon
          value="like"
          :color="btnColor('like')"
          @click="setReaction('like')"
        >
          <v-icon>mdi-thumb-up</v-icon>
        </v-btn>
      </v-col>

      <v-col cols="1">
        <reactions-list reaction-type="like" :reactions="message.reactions"/>
      </v-col>

      <v-col cols="3">
        <v-btn
          variant="outlined"
          size="large"
          icon
          value="dislike"
          :color="btnColor('dislike')"
          @click="setReaction('dislike')"
        >
          <v-icon>mdi-thumb-down</v-icon>
        </v-btn>
      </v-col>

      <v-col cols="2">
        <reactions-list reaction-type="dislike" :reactions="message.reactions"/>
      </v-col>
    </v-row>
    {{setCurrentUserReaction(message)}}
  </div>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import axios from "axios";
  import {mapGetters} from "vuex";
  import ReactionsList from "@/components/chat/messages/ReactionsList.vue"; // TODO: REACTIONS LIST https://codepen.io/betanet/pen/gOxKZMm
  export default {
    name: "ReactionsBlock",
    components: {
      'reactions-list' : ReactionsList,
    },
    data: () => ({
      like: null,
      dislike: null,
      current: null
    }),
    props: {
      message: {
        type: Object,
        required: true
      }
    },
    user() {
      return this.$store.state.user.data
    },
    methods: {
      btnColor(reaction) {
        if (reaction === 'dislike') {
          if (this.dislike) {
            this.current = 'dislike'
            return 'info'
          }
        } else if (reaction === 'like') {
          if (this.like) {
            this.current = 'like'
            return 'info'
          }
        }
      },
      getReactionsCount(message, type) {
        if (message.reactions) {
          return message.reactions.reduce((total, x) => total + (x.type === type), 0)
        } else {
          return 0
        }
      },
      setCurrentUserReaction(message) {
        if (this.message.reactions) {
          const i = this.message.reactions.findIndex(e => e.author.id === this.$store.state.user.data.id);
          if (i > -1) {
            if (this.message.reactions[i].type === 'like') {
              this.dislike = null
              this.like = true
            } else if (this.message.reactions[i].type === 'dislike') {
              this.dislike = true
              this.like = null
            } else {
              this.dislike = null
              this.like = null
            }
          }
        }
      },
      setReaction(reaction) {
        const data = new FormData()
        data.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
        data.append("type", reaction)
        data.append("author", this.$store.state.user.data.id)
        data.append("message", this.message.id)
        axios({
              method: 'post',
              url: 'http://localhost:8000/api/reactions/',
              data: data,
              withCredentials: true,
              header: {
                'Accept': 'application/json',
                'Content-Type': 'multipart/form-data',
              },
        })
        this.$store.dispatch("chat/fetchMessages", {chat: this.$store.state.user.chatId})
        if (reaction === this.current) {
          this.current = null
          this.like = null
          this.dislike = null
        }
      }
    },
    computed: {
      backgroundColor() {
        if (this.current) {
          return 'info'
        } else {
          return ''
        }
      }
    }
  }
</script>

<style scoped>

</style>
