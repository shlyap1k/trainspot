<template>
  <v-row>
    <v-col cols="9">
      <v-card>
        <v-responsive aspect-ratio="16/9">
          <v-card-title>
            Трансляция с веб-камеры
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col>
                <video playsinline autoplay muted id="video"></video>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3">
                <v-btn v-if="!started" v-on:click="startStreaming" color="#80CBC4">
                  Начать трансляцию
                </v-btn>
                <v-btn v-else v-on:click="stopStreaming" color="#EF9A9A">
                  Завершить трансляцию
                </v-btn>
              </v-col>
              <v-col cols="3" v-if="!started">
                <v-text-field
                  label="Название трансляции"
                  v-model="streamName"
                  solo
                ></v-text-field>
              </v-col>
              <v-col cols="3" v-else>
                {{streamName}}
              </v-col>
              <v-col cols="3">
                Длительность трансляции: {{("0" + (time/3600>>0)).slice(-2)
                }}:{{("0" + (time/60>>0)).slice(-2)
                }}:{{("0" + Number(((time/60-(time/60>>0))*60).toFixed(0))).slice(-2)}}
              </v-col>
              <v-col cols="3">
                <v-icon color="#F44336">mdi-account-outline</v-icon> <span class="red--text">{{viewers}}</span>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <section class="select">
                  <label for="audioSource">Источник аудио: </label>
                  <select id="audioSource"></select>
                </section>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <section class="select">
                  <label for="videoSource">Источник видео: </label>
                  <select id="videoSource"></select>
                </section>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
          </v-card-actions>
        </v-responsive>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
  import { io } from "socket.io-client";
  export default {
    name: "BroadcastingVideo",
    data() {
      return {
        time: 0,
        interval: null,
        streamName: 'Прямая трансляция',
        viewers: 0,
        started: false,
        peerConnections: {},
        config: {
          iceServers: [
            {
              "urls": "stun:stun.l.google.com:19302",
            }
          ]
        },
        socket: io.connect('http://localhost:4000/'),
        videoElement: document.querySelector("video"),
        audioSelect: document.querySelector("select#audioSource"),
        videoSelect: document.querySelector("select#videoSource"),

      }
    },
    mounted() {


    },
    methods: {
      toggleTimer() {
        if (this.started) {
          clearInterval(this.interval);
          console.log('timer stops');
        } else {
          this.interval = setInterval(this.incrementTime, 1000);
        }
        this.isRunning = !this.isRunning
      },
      incrementTime() {
        this.time = parseInt(this.time) + 1;
      },
      stopStreaming() {
        console.log('stop streaming')
        this.toggleTimer()
        this.time=0
        this.videoElement.srcObject = null
        this.started = false
        Object.entries(this.peerConnections).forEach(([key, value]) => {
           value.close()
        });
        this.viewers = 0
        console.log('end of stream')
        this.socket.emit("endOfStream", {})
      },
      startStreaming() {
        console.log('start of stream')
        this.toggleTimer()
        this.started = true
        this.socket.on("answer", (id, description) => {
          this.peerConnections[id].setRemoteDescription(description)
        })

        this.socket.on("watcher", id => {
          this.viewers += 1
          this.socket.emit("viewers", {
            viewers: this.viewers,
            time: this.time,
            name: this.streamName
          })
          const peerConnection = new RTCPeerConnection(this.config)
          this.peerConnections[id] = peerConnection

          let stream = this.videoElement.srcObject
          stream.getTracks().forEach(track => peerConnection.addTrack(track, stream))

          peerConnection.onicecandidate = event => {
            if (event.candidate) {
              this.socket.emit("candidate", id, event.candidate)
            }
          };

          peerConnection
            .createOffer()
            .then(sdp => peerConnection.setLocalDescription(sdp))
            .then(() => {
              this.socket.emit("offer", id, peerConnection.localDescription)
            });
        })

        this.socket.on("candidate", (id, candidate) => {
          this.peerConnections[id].addIceCandidate(new RTCIceCandidate(candidate));
        });

        this.socket.on("disconnectPeer", id => {
          this.viewers -= 1
          this.socket.emit("viewers", {viewers: this.viewers})
          this.peerConnections[id].close();
          delete this.peerConnections[id];
        });

        window.onunload = window.onbeforeunload = () => {
          this.socket.close();
        };

        this.videoElement = document.querySelector("video");
        this.audioSelect = document.querySelector("select#audioSource");
        this.videoSelect = document.querySelector("select#videoSource");

        this.audioSelect.onchange = this.getStream
        this.videoSelect.onchange = this.getStream

        this.getStream()
          .then(this.getDevices)
          .then(this.gotDevices)
      },
      getDevices() {
        return navigator.mediaDevices.enumerateDevices();
      },
      gotDevices(deviceInfos) {
        window.deviceInfos = deviceInfos;
        for (const deviceInfo of deviceInfos) {
          const option = document.createElement("option");
          option.value = deviceInfo.deviceId;
          if (deviceInfo.kind === "audioinput") {
            option.text = deviceInfo.label || `Microphone ${this.audioSelect.length + 1}`;
            this.audioSelect.appendChild(option);
          } else if (deviceInfo.kind === "videoinput") {
            option.text = deviceInfo.label || `Camera ${this.videoSelect.length + 1}`;
            this.videoSelect.appendChild(option);
          }
        }
      },
      getStream() {
        if (window.stream) {
          window.stream.getTracks().forEach(track => {
            track.stop();
          });
        }
        const audioSource = this.audioSelect.value;
        const videoSource = this.videoSelect.value;
        const constraints = {
          audio: { deviceId: audioSource ? { exact: audioSource } : undefined },
          video: { deviceId: videoSource ? { exact: videoSource } : undefined }
        };
        return navigator.mediaDevices
          .getUserMedia(constraints)
          .then(this.gotStream)
          .catch(this.handleError);
      },
      gotStream(stream) {
        window.stream = stream;
        this.audioSelect.selectedIndex = [...this.audioSelect.options].findIndex(
          option => option.text === stream.getAudioTracks()[0].label
        );
        this.videoSelect.selectedIndex = [...this.videoSelect.options].findIndex(
          option => option.text === stream.getVideoTracks()[0].label
        );
        this.videoElement.srcObject = stream;
        this.socket.emit("broadcaster");
      },
      handleError(error) {
        console.error("Error: ", error);
      }
    }
  }
</script>

<style scoped>
#video{
  width:100%;
  height:100%;
}
</style>
