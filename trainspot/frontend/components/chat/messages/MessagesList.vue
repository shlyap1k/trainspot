<template>
<div>
  <v-card>
    <v-card-title>Сообщения</v-card-title>
    <v-card-text>{{messages}}</v-card-text>
  </v-card>
</div>
</template>

<script>

  export default {
    name: "MessagesList",
    props: {
      messages: {
        type: Array,
        required: true
      },
    }
  }
</script>

