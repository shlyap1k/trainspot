import Pusher, { Channel, ChannelAuthorizationCallback, Options } from 'pusher-js'
import axios from 'axios'

function getPusher(xsrfToken) {
  Pusher.logToConsole = true;
  const authorizer = (channel, options) => {
      return {
        authorize: (socketId, callback) => {
          const data = new FormData();
          data.append("csrfmiddlewaretoken", xsrfToken)
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
  const pusher = new Pusher('25f45edee24cb9aa5217', {
      cluster: 'eu',
      authorizer: authorizer
    });
  return pusher
}

export default getPusher
