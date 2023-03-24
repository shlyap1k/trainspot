<template>
  <div class="content">
    <slot>
      <v-card>
        <v-card-title>
          Добавление пользователя в чат
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="addUser">
            <v-select
              v-model="selectedUser"
              :items="users"
              item-text="username"
              attach
              label="Найти пользователя"
              return-object
            >
              <template v-slot:prepend-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-text-field
                      v-model="searchTerm"
                      placeholder="Введите логин пользователя"
                      @input="searchUsers"
                    >
                    </v-text-field>
                  </v-list-item-content>
                </v-list-item>
                <v-divider
                  class="mt-2"
                >
                </v-divider>
              </template>
            </v-select>
            <v-btn
              @click="addUser"
            >
              Добавить пользователя
            </v-btn>
            <v-btn
              @click="$emit('cancel')"
            >
              Отмена
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </slot>
  </div>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import axios from "axios";

  export default {
    name: "AddUserForm",
    props: {
    },
    data() {
      return {
        searchTerm: null,
        users: [],
        usersCopy: [],
        selectedUser: null,
        formAdd: new FormData(),
        chat: null
      }
    },
    mounted() {
      apiClient
        .get('users/')
        .then((response) => {
          console.log(response.data)
          this.users = response.data.results.map(user => {
            return user
          })
        })
      this.usersCopy = [...this.users];
    },
    methods: {
      searchUsers (e) {
        this.usersCopy = [...this.users];
        if (!this.searchTerm) {
          this.users = this.usersCopy;
          apiClient
          .get('users/')
          .then((response) => {
            this.users = response.data.results.map(user => {
              return user
            })
          })
        }
        this.users = this.usersCopy.filter(user => {
          return user.username.toLowerCase().indexOf(this.searchTerm.toLowerCase()) > -1
        })
      },
      addUser() {
        let m
        m = this.$store.state.chat.members.map(member => {
          return member.id
        })
        if (!m.includes(this.selectedUser.id))
        {
          const chatId = this.$store.state.user.chatId
          this.$store.state.user.chats.forEach(c => {
            if (c.id === chatId) {
              this.chat = c
            }
          })
          this.formAdd.append("creator", this.chat.creator.id)
          this.formAdd.append("name", this.chat.name)
          m.forEach(userId => this.formAdd.append("members", userId));
          this.formAdd.append("members", this.selectedUser.id)
          axios({
            method: 'put',
            url: 'http://localhost:8000/api/chats/'+chatId+'/',
            data: this.formAdd,
            withCredentials: true,
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'multipart/form-data',
              'X-CSRFToken': this.$cookies.get("XSRF-TOKEN")
            },
          })
          this.$store.dispatch("chat/fetchMessages", {chat: chatId})
          this.$store.dispatch('user/fetchChats')
        }
      }

    }
  }
</script>

