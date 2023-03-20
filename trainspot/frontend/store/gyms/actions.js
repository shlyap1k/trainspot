import apiClient from "@/src/apiClient";

export default {
  fetchGyms({ commit }) {
    apiClient
      .get("gyms/")
      .then(response => {
        commit("setGyms", response.data.results)
        })
      .catch(e => {
        console.log(e)
      })
  }
}
