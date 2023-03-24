import apiClient from "@/src/apiClient";

export default {
  unsetReply({commit}) {
    commit("setAnswerTo", null)
  },
  replyToMessage({commit}, payload) {
    if (payload.message_id) {
      apiClient
        .get("messages/" + payload.message_id + '/')
        .then(response => {

        commit("setAnswerTo", response.data)
        })
        .catch(e => {
          console.log(e)
        })
    }
  },
  fetchMessages({ commit }, payload) {
    if (payload.chat) {
      apiClient
        .get("chats/" + payload.chat + '/')
        .then(response => {
          commit("setChat", response.data)
          commit("setMessages", response.data.messages)
          commit("setMembers", response.data.members)
        })
        .catch(e => {
          console.log(e)
        })
    }
  }
}
