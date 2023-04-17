<template>
  <div>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <h1>
          Рассылки
          <v-btn
            v-if="role==='admin'"
            icon
            @click="openForm"
          >
            <v-icon>
              mdi-plus
            </v-icon>
          </v-btn>
        </h1>
        <v-dialog v-model="dialog" max-width="500px">
          <mailing-list-form @created="fetchMailingLists" @close="closeForm"></mailing-list-form>
        </v-dialog>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" sm="6" md="6">
        <v-card v-for="mailing in mailingLists" :key="mailing.id">
          <v-card-title>
            {{ mailing.name }}
            <v-spacer></v-spacer>
            <v-btn
              icon
              @click="deleteMailing(mailing.id)"
              v-if="role==='admin'"
              color="red"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-subtitle v-if="role==='admin'">
            Количество разосланных писем по этой теме: {{countMailings(mailing.id)}}
          </v-card-subtitle>

          <v-card-text>
            {{ mailing.description }}
          </v-card-text>
          <v-card-actions>
            <v-btn
              text
              color="teal accent-4"
              @click="subscribe(mailing.id)"
              v-if="!isSubscribed(mailing.id)"
            >
              Подписаться
            </v-btn>
            <v-btn
              text
              color="pink accent-4"
              @click="unsubscribe(mailing.id)"
              v-if="isSubscribed(mailing.id)"
            >
              Отписаться
            </v-btn>
            <v-btn
              text
              color="primary"
              @click="openMailing(mailing.id)"
              v-if="role==='admin'"
            >
              Провести рассылку
            </v-btn>
          </v-card-actions>
        </v-card>
        <v-dialog v-model="mailingDialog" max-width="500px">
          <do-mailing @close="mailingDialog=false" :mailing="selectedMailing"></do-mailing>
        </v-dialog>
        <v-spacer></v-spacer>
      </v-col>
    </v-row>
    <v-row justify="center" v-if="mailingLists.length === 0">
      <v-col cols="12" sm="8" md="6">
        Рассылок пока что нет...
      </v-col>
    </v-row>

  </div>
</template>

<script>

  import apiClient from "@/src/apiClient";
  import MailingListForm from "@/components/MailingListForm.vue";
  import DoMailing from "@/components/DoMailing.vue";
  import axios from "axios";
  import {mapGetters} from "vuex";

  export default {
  name: "Mailings",
  components: {
    MailingListForm,
    DoMailing
  },
  data: () => ({
    reveal: false,
    mailingLists: [],
    dialog: false,
    mailingDialog: false,
    selectedMailing: null,
    mailings: []
  }),
  computed: {
    role() { return this.$store.state.user.role },
    ...mapGetters({
      user: 'user/getUser'
    })
  },
  mounted() {
    this.fetchMailingLists();
    this.fetchMailings();
  },
  methods: {
    countMailings(id) {
      return this.mailings.filter(mail => mail.list === id).length
    },
    openMailing(id) {
      this.selectedMailing = this.mailingLists.find(item => item.id === id)
      this.mailingDialog = true
    },
    unsubscribe(id) {
      // Метод для подписки на рассылку
      const formData = new FormData();
      formData.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
      axios({
            method: 'post',
            url: `http://localhost:8000/api/mailinglists/${id}/unsubscribe/`,
            data: formData,
            withCredentials: true,
            header: {
              'Accept': 'application/json',
              'Content-Type': 'multipart/form-data',
            },
          })
        .then(() => {
          this.fetchMailingLists(); // Обновляем список рассылок после успешной подписки
        })
        .catch(error => {
          console.error(`Ошибка при подписке на рассылку с ID: ${id}`, error);
        });
    },
    subscribe(id) {
      // Метод для подписки на рассылку
      const formData = new FormData();
      formData.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
      axios({
            method: 'post',
            url: `http://localhost:8000/api/mailinglists/${id}/subscribe/`,
            data: formData,
            withCredentials: true,
            header: {
              'Accept': 'application/json',
              'Content-Type': 'multipart/form-data',
            },
          })
        .then(() => {
          this.fetchMailingLists(); // Обновляем список рассылок после успешной подписки
        })
        .catch(error => {
          console.error(`Ошибка при подписке на рассылку с ID: ${id}`, error);
        });
    },
    isSubscribed(id) {
      if (this.user) {
        const mailing = this.mailingLists.find(item => item.id === id)
        return mailing.subscribers.some(s => s.id === this.user.id);
      }
      return false;
    },
    async fetchMailings() {
       this.mailings = await this.fetchData('mailing/');
    },
    async fetchMailingLists() {
      this.mailingLists = await this.fetchData('mailinglists/');
    },
    async fetchData(url) {
      try {
        let allData = []; // Массив для хранения данных со всех страниц
        let nextUrl = url; // Следующая страница API (начальное значение равно переданному URL)

        // Используем цикл, чтобы получить данные со всех страниц
        while (nextUrl !== null) {
          const response = await apiClient.get(nextUrl); // Выполняем GET-запрос на текущую страницу
          allData = allData.concat(response.data.results); // Добавляем данные текущей страницы в массив с общими данными
          nextUrl = response.data.next; // Обновляем URL следующей страницы
        }

        return allData; // Возвращаем все данные
      } catch (error) {
        console.error("Ошибка при получении данных:", error);
        throw error; // Пробрасываем ошибку дальше
      }
    },
    openForm() {
      this.dialog = true;
    },
    closeForm() {
      this.dialog = false; // Закрываем диалоговое окно с формой
    },
    deleteMailing(mailing_id) {
      const formData = new FormData(); // TODO: НЕ УДАЛЯЕЦА((((
      formData.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))

      axios({
            method: 'delete',
            url: 'http://localhost:8000/api/mailinglists/'+mailing_id+'/',
            data: formData,
            withCredentials: true,
            header: {
              'Accept': 'application/json',
              'Content-Type': 'multipart/form-data',
            },
          })
      .then(response => {
          // Обработка успешного создания рассылки
          console.log("Рассылка успешно удалена", response);
          this.$emit("created"); // Используем событие для обновления списка рассылок в родительском компоненте
          this.closeForm();
        })
        .catch(error => {
          // Обработка ошибки при создании рассылки
          console.error("Ошибка при удалении рассылки", error);
        });
    }
  }
}
</script>

