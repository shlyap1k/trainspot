import apiClient from "@/src/apiClient";
import state from "@/store/user/state";

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
  fetchSubscription({ commit }) {
    apiClient.get("subscriptions/1/")
      .then(response =>{
        commit("setUserSubscription", response.data)
        })
      .catch(e => {
        console.log(e)
      })
  },
  logoutUser({ commit }) {
    commit("resetUserData")
  }

}
