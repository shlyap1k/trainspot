<template>
  <v-card>
    <v-card-title>
      Создание рассылки
    </v-card-title>
    <v-card-text>
      <v-form ref="form" @submit.prevent="createMailingList">
        <v-text-field
          v-model="form.name"
          label="Название"
          required
        ></v-text-field>
        <v-textarea
          v-model="form.description"
          label="Описание"
          required
        ></v-textarea>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn type="submit" color="primary">Создать</v-btn>
          <v-btn type="button" @click="closeForm">Отмена</v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import apiClient from "@/src/apiClient";
import axios from "axios";

export default {
  name: "MailingListForm",
  data: () => ({
    form: {
      name: "",
      description: ""
    }
  }),
  methods: {
    createMailingList() {
      const formData = new FormData();
      formData.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
      formData.append("name", this.form.name);
      formData.append("creator", this.$store.state.user.data.id);
      formData.append("description", this.form.description);

      axios({
            method: 'post',
            url: 'http://localhost:8000/api/mailinglists/',
            data: formData,
            withCredentials: true,
            header: {
              'Accept': 'application/json',
              'Content-Type': 'multipart/form-data',
            },
          })
      .then(response => {
          // Обработка успешного создания рассылки
          console.log("Рассылка успешно создана", response);
          this.$emit("created"); // Используем событие для обновления списка рассылок в родительском компоненте
          this.closeForm();
        })
        .catch(error => {
          // Обработка ошибки при создании рассылки
          console.error("Ошибка при создании рассылки", error);
        });
    },
    closeForm() {
      this.$emit("close"); // Используем событие для закрытия формы в родительском компоненте
    }
  }
};
</script>
