<template>
  <v-row>
    <v-col>
      <video ref="localVideo" autoplay></video>
    </v-col>
    <v-col>
      <video ref="remoteVideo" autoplay></video>
    </v-col>
  </v-row>
</template>

<script>
import SimplePeer from 'simple-peer';

export default {
  mounted() {
    // Создание экземпляра SimplePeer
    this.peer = new SimplePeer({ initiator: location.hash === '#init' });

    // Установка обработчиков событий
    // this.peer.on('signal', this.onSignal);
    // this.peer.on('stream', this.onStream);

    // Получение видеопотока с камеры
    // get video/voice stream
      navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      }).then(this.gotMedia).catch(() => {})
  },
  methods: {
    gotMedia(stream) {
      var peer1 = new this.peer({ initiator: true, stream: stream })
      var peer2 = new this.peer()
      peer1.on('signal', data => {
        peer2.signal(data)
      })

      peer2.on('signal', data => {
        peer1.signal(data)
      })
      peer2.on('stream', stream => {
        // got remote video stream, now let's show it in a video tag
        var video = document.querySelector('video')

        if ('srcObject' in video) {
          video.srcObject = stream
        } else {
          video.src = window.URL.createObjectURL(stream) // for older browsers
        }

        video.play()
      })

    },
    onSignal(signal) {
      // Отправка сигнала другому пользователю через средство связи (например, сокет)
      console.log('Отправка сигнала:', signal);
    },
    onStream(stream) {
      // Воспроизведение видеопотока от удаленного пользователя
      this.$refs.remoteVideo.srcObject = stream;
    },
  },
};
</script>
