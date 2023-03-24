<template>
  <v-row>
    <v-dialog
      v-model="dialog"
      persistent
      width="512"
    >
      <template v-slot:activator="{ props }">
        <v-btn
          v-bind="props"
          icon
          @click="dialog=true"
        >
          <v-icon>
            mdi-chat-plus
          </v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Создать чат</span>
        </v-card-title>
        <v-form>
          <v-card-text>
            <v-container>
              <v-row>
                <v-text-field
                  label="Название чата*"
                  v-model="chatName"
                  required
                ></v-text-field>
              </v-row>
            </v-container>
            <small>*обязательно для заполнения</small>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="blue-darken-1"
              variant="text"
              @click="dialog = false"
            >
              Закрыть
            </v-btn>
            <v-btn
              color="blue-darken-1"
              variant="text"
              @click="createChat"
            >
              Создать
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
  import axios from "axios";

  export default {
    name: "",
    data: () => ({
      dialog: false,
      chatName: null
    }),
    methods: {
      createChat() {
        this.dialog = false
        const data = new FormData()
        data.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
        data.append("name", this.chatName)
        data.append("creator", this.$store.state.user.data.id)
        data.append("members", this.$store.state.user.data.id)
        axios({
              method: 'post',
              url: 'http://localhost:8000/api/chats/',
              data: data,
              withCredentials: true,
              header: {
                'Accept': 'application/json',
                'Content-Type': 'multipart/form-data',
              },
        })
        this.chatName = null
        this.$store.dispatch('user/fetchChats')
      }
    }
  }
</script>

<style scoped>

</style>
