import apiClient from "@/src/apiClient";

export default {
  setAnswerTo(state, answer_to) {
    state.answer_to = answer_to
  },
  setChat(state, chatData) {
    state.chat = chatData
  },
  setMessages(state, messagesData) {
    state.messages = messagesData.map(message => {
      return {
        id: message.id,
        text: message.text,
        author: message.author,
        chat: message.chat,
        parent: message.parent,
        reactions: message.reactions
      }
    })
  },
    setMembers(state, membersData) {
      state.members = membersData.map(member => {
        return {
          id: member.id,
          username: member.username,
          first_name: member.first_name,
          last_name: member.last_name,
          email: member.email,
          role: member.role
        }
      })
  },
}
