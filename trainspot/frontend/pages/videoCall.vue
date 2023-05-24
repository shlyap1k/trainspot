<template>
  <div>
    <h1>Видеозвонок</h1>
    <VideoCall />
  </div>
</template>

<script>
import VideoCall from '@/components/streams/VideoCall.vue';

export default {
  components: {
    VideoCall,
  },
};
</script>
