import apiClient from "@/src/apiClient";

export default {
  setUserData(state, userData) {
    state.data = userData
  },
  setUserRole(state, role) {
    state.role = role
  },
  setUserSubscription(state, subData) {
    state.subscription = subData
  },
  setChats(state, chatsData) {
    state.chats = chatsData.map(chat => {
      return {
        id: chat.id,
        name: chat.name,
        creator: chat.creator,
        members: chat.members,
        messages: chat.messages
      }
    })
  },
  resetUserData(state) {
    state.data = null
    state.role = null
    state.subscription = null
    state.chats = null
    state.chatId = null
  },
  setCurrentChat(state, chatId) {
    state.chatId = chatId
  }
}
