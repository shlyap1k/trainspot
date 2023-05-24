<template>
  <v-card>
    <v-card-text>
      <span id="myid"></span>
      <video ref="selfview" autoplay></video>
      <video id="remoteview"></video>
      <v-btn id="endCall" style="display: none;" onclick="endCurrentCall()">End Call </v-btn>
      <div id="list">
          <ul id="users">
            <li v-for="user in users">
              {{user}}
            </li>
          </ul>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import Pusher, { Channel, ChannelAuthorizationCallback, Options } from 'pusher-js'
import axios from 'axios'
import {mapGetters} from "vuex";
export default {
  name: 'VideoPublisher',
  components: {
  },
  mounted() {
    console.log("MOUNTED")
    Pusher.logToConsole = true;
    const data = new FormData();
    console.log(this.$cookies.getAll())
    data.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
    const csrf = this.$cookies.get("XSRF-TOKEN")
    console.log(csrf)



    const authorizer = (channel, options) => {
      return {
        authorize: (socketId, callback) => {
          data.append("channel_name", channel.name)
          data.append("socket_id", socketId)
          axios({
            method: 'post',
            url: 'http://localhost:8000/pusher_auth', // TODO: УБРАТЬ ЛОКАЛХОСТЫ
            data: data,
            withCredentials: true
          })
            .then((response) => {
              callback(null, response.data)
            })
            .catch((error) => {
              callback(new Error(`Error authenticating with server: ${error}`), {
                auth: ''
              })
            })
        }
      }
    }



    this.pusher = new Pusher('key', {
      cluster: 'a',
      authEndpoint: '',
      authorizer: authorizer
    });
    //
    this.channel = this.pusher.subscribe("presence-video")

    this.channel.bind("pusher:subscription_succeeded", members => {
      //set the member count
      console.log(members)
      this.usersOnline = members.count;
      this.id = this.channel.members.me.id;
      document.getElementById("myid").innerHTML = ` My caller id is : ` + this.id;
      members.each(member => {
        if (member.id != this.channel.members.me.id) {
          this.users.push(member.id);
        }
      });
      this.render();
    });

    this.channel.bind("pusher:member_added", member => {
      this.users.push(member.id);
      this.render();
    });

    this.channel.bind("pusher:member_removed", member => {
      // for remove member from list:
      var index = users.indexOf(member.id);
      this.users.splice(index, 1);
      if (member.id == this.room) {
        this.endCall();
      }
      this.render();
    });

    this.GetRTCPeerConnection();
    this.GetRTCSessionDescription();
    this.GetRTCIceCandidate();
    this.prepareCaller();

    //Listening for the candidate message from a peer sent from onicecandidate handler
    this.channel.bind("client-candidate", function(msg) {
      if (msg.room == this.room) {
        console.log("candidate received");
        this.caller.addIceCandidate(new RTCIceCandidate(msg.candidate));
      }
    });

    //Listening for Session Description Protocol message with session details from remote peer
    this.channel.bind("client-sdp", function(msg) {
      if (msg.room == this.id) {
        console.log("sdp received");
        var answer = confirm(
          "You have a call from: " + msg.from + "Would you like to answer?"
        );
        if (!answer) {
          return this.channel.trigger("client-reject", { room: msg.room, rejected: this.id });
        }
        this.room = msg.room;
        getCam()
          .then(stream => {
            this.localUserMedia = stream;
            this.toggleEndCallButton();
            this.$refs.selfview.srcObject = stream
            this.caller.addStream(stream);
            var sessionDesc = new RTCSessionDescription(msg.sdp);
            this.caller.setRemoteDescription(sessionDesc);
            this.caller.createAnswer().then(function(sdp) {
              this.caller.setLocalDescription(new RTCSessionDescription(sdp));
              this.channel.trigger("client-answer", {
                sdp: sdp,
                room: this.room
              });
            });
          })
          .catch(error => {
            console.log("an error occured", error);
          });
      }
    });

    //Listening for answer to offer sent to remote peer
    this.channel.bind("client-answer", function(answer) {
      if (answer.room == this.room) {
        console.log("answer received");
        this.caller.setRemoteDescription(new RTCSessionDescription(answer.sdp));
      }
    });

    this.channel.bind("client-reject", function(answer) {
      if (answer.room == this.room) {
        console.log("Call declined");
        alert("call to " + answer.rejected + "was politely declined");
        this.endCall();
      }
    });

    this.channel.bind("client-endcall", function(answer) {
      if (answer.room == this.room) {
        console.log("Call Ended");
        this.endCall();
      }
    });

  },
  methods: {
    render() {
      var list = "";
      this.users.forEach(function(user) {
        list +=
          `<li>` +
          user +
          ` <input type="button" style="float:right;"  value="Call" onclick="callUser('` +
          user +
          `')" id="makeCall" /></li>`;
      });
      document.getElementById("users").innerHTML = list;
    },
    prepareCaller() {
      //Initializing a peer connection
      this.caller = new window.RTCPeerConnection();
      //Listen for ICE Candidates and send them to remote peers
      this.caller.onicecandidate = function(evt) {
        if (!evt.candidate) return;
        console.log("onicecandidate called");
        onIceCandidate(this.caller, evt);
      };
      //onaddstream handler to receive remote feed and show in remoteview video element
      this.caller.onaddstream = function(evt) {
        console.log("onaddstream called");
        if (window.URL) {
          document.getElementById("remoteview").src = window.URL.createObjectURL(
            evt.stream
          );
        } else {
          document.getElementById("remoteview").src = evt.stream;
        }
      };
    },
    getCam() {
      //Get local audio/video feed and show it in selfview video element
      return navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      });
    },
    GetRTCIceCandidate() {
      window.RTCIceCandidate =
        window.RTCIceCandidate ||
        window.webkitRTCIceCandidate ||
        window.mozRTCIceCandidate ||
        window.msRTCIceCandidate;
      return window.RTCIceCandidate;
    },
    GetRTCPeerConnection() {
      window.RTCPeerConnection =
        window.RTCPeerConnection ||
        window.webkitRTCPeerConnection ||
        window.mozRTCPeerConnection ||
        window.msRTCPeerConnection;
      return window.RTCPeerConnection;
    },
    GetRTCSessionDescription() {
      window.RTCSessionDescription =
        window.RTCSessionDescription ||
        window.webkitRTCSessionDescription ||
        window.mozRTCSessionDescription ||
        window.msRTCSessionDescription;
      return window.RTCSessionDescription;
    },
    callUser(user) {
      this.getCam()
        .then(stream => {
          if (window.URL) {
            document.getElementById("selfview").src = window.URL.createObjectURL(
              stream
            );
          } else {
            document.getElementById("selfview").src = stream;
          }
          this.toggleEndCallButton();
          this.caller.addStream(stream);
          this.localUserMedia = stream;
          this.caller.createOffer().then(function(desc) {
            this.caller.setLocalDescription(new RTCSessionDescription(desc));
            this.channel.trigger("client-sdp", {
              sdp: this.desc,
              room: this.user,
              from: this.id
            });
            this.room = this.user;
          });
        })
        .catch(error => {
          console.log("an error occured", error);
        });
    },
    endCall() {
      this.room = undefined;
      this.caller.close();
      for (let track of localUserMedia.getTracks()) {
        track.stop();
      }
      this.prepareCaller();
      this.toggleEndCallButton();
    },
    endCurrentCall() {
      this.channel.trigger("client-endcall", {
        room: this.room
      });
      this.endCall();
    },
    onIceCandidate(peer, evt) {
      if (evt.candidate) {
        this.channel.trigger("client-candidate", {
          candidate: evt.candidate,
          room: this.room
        });
      }
    },
    toggleEndCallButton() {
      if (document.getElementById("endCall").style.display == "block") {
        document.getElementById("endCall").style.display = "none";
      } else {
        document.getElementById("endCall").style.display = "block";
      }
    }
  },
  computed: {
    ...mapGetters({
      user: 'user/getUser'
    })
  },
  data() {
    return {
      pusher: null,
      channel: null,
      usersOnline: 0,
      sessionDesc: null,
      currentCaller: null,
      room: null,
      localUserMedia: null,
      id: null,
      users: []
    }
  }
};
</script>

<style scoped>
video {
  width: 100%;
  max-width: 400px;
}
</style>
