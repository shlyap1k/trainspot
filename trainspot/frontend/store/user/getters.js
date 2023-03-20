export default {
  getUser(state) {
    return state.data
  },

  getRole(state) {
    return state.role
  },

  getSubscription(state) {
    return state.subscription
  },
  getChats(state) {
    return state.chats
  },
  getChatId(state) {
    return state.chatId
  }
}

