<template>
  <v-row>
    <v-col>
      <broadcasting-video/>
    </v-col>
  </v-row>
</template>

<script>
  import BroadcastingVideo from "@/components/streams/BroadcastingVideo.vue";
  export default {
    components: {BroadcastingVideo},
    name: "broadcaster"
  }
</script>

<style scoped>

</style>
