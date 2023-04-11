<template>
  <v-card>
    <v-card-title>
      Проведение рассылки {{mailing.name}}
    </v-card-title>
    <v-card-subtitle>
      {{mailing.description}}
    </v-card-subtitle>
    <v-card-text>
      <v-form ref="form" @submit.prevent="createMailing">
        <v-text-field
          v-model="form.subject"
          label="Тема"
          required
        ></v-text-field>
        <v-textarea
          v-model="form.content"
          label="Текст"
          required
        ></v-textarea>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn type="submit" color="primary">Отправить</v-btn>
          <v-btn type="button" @click="closeForm">Отмена</v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  name: "DoMailing",
  props: {
    mailing: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    form: {
      subject: "",
      content: ""
    }
  }),
  methods: {
    createMailing() {
      const formData = new FormData();
      formData.append("csrfmiddlewaretoken", this.$cookies.get("XSRF-TOKEN"))
      formData.append("subject", this.form.subject);
      formData.append("list", this.mailing.id);
      formData.append("content", this.form.content);

      axios({
            method: 'post',
            url: 'http://localhost:8000/api/mailing/',
            data: formData,
            withCredentials: true,
            header: {
              'Accept': 'application/json',
              'Content-Type': 'multipart/form-data',
            },
          })
      .then(response => {
          console.log("Рассылка успешно проведена", response);
          this.$emit("created");
          this.closeForm();
        })
        .catch(error => {
          console.error("Ошибка при проведении рассылки", error);
        });
    },
    closeForm() {
      this.$emit("close");
    }
  }
};
</script>
