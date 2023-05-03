<template>
  <div>
    <video ref="video" autoPlay></video>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        ws: null
      }
    },
    mounted() {
      this.ws = new WebSocket('ws://localhost:8000/ws/video/stream/');
      this.ws.addEventListener('open', (event) => {
        console.log('WebSocket connection established.');
      });
      this.ws.addEventListener('message', (event) => {
        const message = JSON.parse(event.data);
        if (message.type === 'video') {
          this.$refs.video.src = message.dataURL;
        }
      });
    },
    beforeDestroy() {
      this.ws.close();
      console.log('WebSocket connection closed.');
    }
  }
</script>
