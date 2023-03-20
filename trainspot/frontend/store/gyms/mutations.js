import apiClient from "@/src/apiClient";

export default {
  setGyms(state, gymsData) {
      state.gyms = gymsData.map(gym => {
        return {
          id: gym.id,
          name: gym.name,
          address: gym.address,
          users: gym.users
        }
      })
  },
}
