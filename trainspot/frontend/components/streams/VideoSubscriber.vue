<template>
  <div>
    <h2>Просмотр видео</h2>
    <video ref="videoRef" autoplay></video>
  </div>
</template>

<script>
import Pusher from 'pusher-js';
import {mapGetters} from "vuex";

export default {
  name: 'VideoSubscriber',
  mounted() {
    const csrf = this.$cookies.get("XSRF-TOKEN")
    // Инициализация клиента Pusher
    const pusher = new Pusher('key', {
      cluster: 'a',
      authEndpoint: 'http://localhost:8000/pusher_auth',
      app_name: 'trainspot-development',
      auth: {
        headers: {
          'X-CSRFToken': csrf
        }
  }
    });
    Pusher.logToConsole = true;

    // Создание нового канала Pusher
    const channel = pusher.subscribe('video-channel');

    const videoStreamChannel = channel.bind('client-video-stream',);
    videoStreamChannel.emit('stream', {
      test:'aboba'
    });

  },
  computed: {
    ...mapGetters({
      user: "user/getUser"
    })
  }
};
</script>

<style scoped>
video {
  width: 100%;
  max-width: 400px;
}
</style>
