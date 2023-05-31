<template>
  <v-row>
    <v-col>
      <watching-video/>
    </v-col>
  </v-row>
</template>

<script>
  import WatchingVideo from "@/components/streams/WatchingVideo.vue";
  export default {
    name: "viewer",
    components: {WatchingVideo}
  }
</script>

<style scoped>

</style>
