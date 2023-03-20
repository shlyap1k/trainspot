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
  resetUserData(state) {
    state.data = null
    state.role = null
    state.subscription = null
  }
}
