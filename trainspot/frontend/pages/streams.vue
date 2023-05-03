<template>
  <div>
  <button @click="startBroadcast">Start Broadcast</button>
  <video ref="localVideo" autoplay></video>
  <video ref="remoteVideo" autoplay></video>
  </div>
</template>

<script>
import axios from 'axios';
import SimplePeer from 'simple-peer';
import ReconnectingWebSocket from 'reconnecting-websocket';

export default {
  data() {
    return {
      // ...
      signalingSocket: null,
    };
  },
  created() {
    // ...
    this.signalingSocket = new ReconnectingWebSocket('ws://localhost:8000/ws/signaling/');
    this.signalingSocket.addEventListener('message', (event) => {
      const data = JSON.parse(event.data);
      // Обработать полученный сигнал
    });
    this.watchStream(1)
  },
  // ...
  methods: {
    // ...
    async startBroadcast() {

      // Получить локальный видеопоток
      const localStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      });
      this.$refs.localVideo.srcObject = localStream;
      // Создать пир для передачи видеопотока
      const peer = new SimplePeer({initiator: true, stream: localStream});

      // Обработка событий пира
      peer.on('signal', async (data) => {
        await axios.post('http://localhost:8000/send_signal/', data);
        console.log(data)
      });

      peer.on('stream', (remoteStream) => {
        this.$refs.remoteVideo.srcObject = remoteStream;
        console.log("WATCHING STREAM")
      });

      // Установить соединение с другими пользователями для просмотра трансляции
      // ...
    },
    async watchStream(streamId) {
      // ...
      // Код для установления соединения с трансляцией через WebRTC
      const peer = new SimplePeer({initiator: false});
      console.log(peer)
      // Обработка событий пира
      peer.on('signal', (data) => {
        this.signalingSocket.send(JSON.stringify(data));
      });
      this.signalingSocket.addEventListener('message', (event) => {
        const data = JSON.parse(event.data);
        peer.signal(data);
      });
      const eventSource = new EventSource('ws://localhost:8000/ws/signaling/');
      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        peer.signal(data);

        // Получить сигналы от сервера и установить соединение с пиром
        // ...
      }
    }
  }
}
</script>
