<template>
  <v-menu
      open-on-click
      offset-y
      :close-on-content-click="false"
      rounded="xl"
      max-width="400"
    >
      <template v-slot:activator="{ on, attrs }">
        <div
          v-bind="attrs"
          v-on="on"
        >
          {{parent.author.first_name + ' ' + parent.author.last_name + ': ' +parent.text.substring(0,25)+".."}}
          <v-divider></v-divider>
        </div>
      </template>
    <div v-if="parent">
<!--      {{parent.text}}-->
    </div>
        <message-block
          v-if="parent"
          :message="parent"
        />
    </v-menu>
</template>

<script>
  import apiClient from '@/src/apiClient'
  // import MessageBlock from '@/components/chat/messages/MessageBlock.vue'
  export default {
    name: 'ShowRelatedMessage',

    components: {
      MessageBlock: () => import('@/components/chat/messages/MessageBlock.vue'),
    },
    props: {
      message: {
        type: Object,
        required: true
      },
      parent: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        parent_message: null
      }
    },
    created() {
      console.log('show related message created ')
    },
    methods: {
    },
  }
</script>

<style scoped>

</style>
