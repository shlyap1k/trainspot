<template>
  <div>
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
    {{getLikesCount(message)}}
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
    {{getDislikesCount(message)}}
    {{setCurrentUserReaction(message)}}
  </div>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import axios from "axios"; // TODO: REACTIONS LIST https://codepen.io/betanet/pen/gOxKZMm
  export default {
    name: "ReactionsBlock",
    data: () => ({
      like: null,
      dislike: null,
      current: null
    }),
    props: {
      message: {
        type: Object,
        required: true
      },
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
      getLikesCount(message) {
        return message.reactions.reduce((total,x) => total+(x.type==='like'), 0)
        // return 2
      },
      getDislikesCount(message) {
        return message.reactions.reduce((total,x) => total+(x.type==='dislike'), 0)
      },
      setCurrentUserReaction(message) {
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
      },
      setReaction(reaction) {
        const data = new FormData()
        data.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
        data.append("type", reaction)
        data.append("author", this.message.author.id)
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
        apiClient.get('messages/' + this.message.id + '/').then(message => this.message = message.data)
        // console.log(this.message)
      }
    }
  }
</script>

<style scoped>

</style>
