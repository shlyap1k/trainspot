<template>
  <v-menu
      open-on-hover
      offset-y
      :close-on-content-click="false"
      rounded="xl"
      max-width="400"
    >
      <template v-slot:activator="{ on, attrs }">
        <div
          v-bind="attrs"
          v-on="on"
        >
          {{membersCount()}}
        </div>
      </template>

      <v-card
        rounded="xl"
      >
        <v-card-subtitle>
          Список участников чата:
        </v-card-subtitle>
        <v-card-text>
          <div v-for="member in members">
            <v-card max-width="300">
              <v-card-title>
                {{member.first_name + ' ' + member.last_name}}
              </v-card-title>
              <v-card-subtitle>
                {{'@' + member.username}}
              </v-card-subtitle>

              <v-card-actions>
                <v-btn
                  @click="deleteUser(member.id)"
                >
                  удалить пользователя из чата
                </v-btn>
              </v-card-actions>

            </v-card>
          </div>
          <v-btn
            @click="openForm"
          >
            добавить пользователя
          </v-btn>
        </v-card-text>
        <AddUserForm
          v-if="formOpened"
          @cancel="formOpened=false"
          @submit="onFormSubmit"
        ></AddUserForm>
      </v-card>
    </v-menu>
</template>

<script>
  import AddUserForm from "@/components/chat/messages/messages_forms/AddUserForm.vue";
  import axios from "axios";
  import ApiClient from "@/src/apiClient";
  import {mapGetters} from "vuex";
  export default {
    name: "MembersList",
    components: {
      AddUserForm
    },
    data() {
      return {
        formOpened: false
      }
    },
    props: {
      members: {
        type: Array,
        required: true
      }
    },
    methods: {
      num_word(value, words) {
        value = Math.abs(value) % 100;
        var num = value % 10;
        if(value > 10 && value < 20) return words[2];
        if(num > 1 && num < 5) return words[1];
        if(num == 1) return words[0];
        return words[2];
      },
      membersCount() {
        let count;
        count = this.members.length
        return count + ' ' + this.num_word(count, ['участник', 'участника', 'участников'])
      },
      openForm() {
        this.formOpened = true
      },
      onFormSubmit () {
        this.formDialog = false
        this.$store.dispatch('user/fetchChats')
      },
      deleteUser(user_id) {
        let m, chat
        const chatId = this.$store.state.user.chatId
          this.$store.state.user.chats.forEach(c => {
            if (c.id === chatId) {
              chat = c
            }
          })
        m = this.$store.state.chat.members.map(member => {
          return member.id
        })
        m = m.filter(uid => uid !== user_id)
        this.formAdd = new FormData()
        this.formAdd.append("creator", chat.creator.id)
        this.formAdd.append("name", chat.name)
        m.forEach(userId => this.formAdd.append("members", userId));
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
        this.$store.dispatch('chat/fetchMessages', {chat: chat.id})
      },
      computed: {
        ...mapGetters({
          members: 'chat/getMembers'
        })
      }
    },
  }
</script>

<style scoped>

</style>
