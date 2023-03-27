import apiClient from "@/src/apiClient"

export default {
  fetchUser({ commit }) {
    apiClient.get("profile/")
      .then(response =>{
        commit("setUserData", response.data)
        commit("setUserRole", response.data.role)
        })
      .catch(e => {
        console.log(e)
      })
  },
  fetchSubscription({ commit }, payload) {
    if (payload) {
      apiClient.get("subscriptions/" + payload.userId + "/")  // TODO: GET USER ID
        .then(response => {
          commit("setUserSubscription", response.data)
        })
        .catch(e => {
          console.log(e)
        })
    }
  },
  logoutUser({ commit }) {
    commit("resetUserData")
  },
  fetchChats({ commit }) {
    apiClient.get("chats/")
      .then(response =>{
        commit("setChats", response.data)
        })
      .catch(e => {
        console.log(e)
      })
  },
  selectCurrentChat({commit}, payload) {
    commit("setCurrentChat", payload.chatId)
  }
}
