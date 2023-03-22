<template>
  <v-card rounded="xl" max-width="400">
<!--     color="#EDE7F6"-->
    <v-card-subtitle>
      <p style="color: red">{{message.author.first_name + ' ' + message.author.last_name}}</p>
    </v-card-subtitle>
    <v-card-text>
      {{message.text}}
    </v-card-text>
    <v-card-actions>
      <reactions-block :message="message"/>
    </v-card-actions>
    <v-spacer></v-spacer>
  </v-card>
</template>

<script>
  import ReactionsBlock from "@/components/chat/messages/ReactionsBlock.vue";
  export default {
    name: "MessageBlock",
    modules: [ReactionsBlock],
    components: {
      'reactions-block' : ReactionsBlock,
    },
    props: {
      message: {
        type: Object,
        required: true
      },
    }
  }
</script>

<style scoped>
  .message-block-style >>> .v-card {
    color: #EDE7F6
  }
</style>
