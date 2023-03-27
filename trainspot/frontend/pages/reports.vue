<template>
<div>
  <div>
    <v-date-picker v-model="date1" :landscape="landscape" :reactive="reactive"></v-date-picker>
    <v-date-picker v-model="date2" :landscape="landscape" :reactive="reactive"></v-date-picker>
  </div>
  <v-btn @click="getpdf()">
    получить файл
  </v-btn>
</div>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import axios from "axios";

  export default {
    name: "reports",
    data() {
      return {
        file: null,
        date1: null,
        date2: null
      }
    },
    methods: {
      getpdf() {
        console.log(this.$store.state.user.data.role)
        console.log(this.date1)
        apiClient
          .get(`financialrecords/1/download/`, {params: {
            start: this.date1,
            end: this.date2
            }})
          .then(response => {
             let fileURL = window.URL.createObjectURL(new Blob([response.data]));
             let fileLink = document.createElement('a');

             fileLink.href = fileURL;
             fileLink.setAttribute('download', 'file.pdf');
             document.body.appendChild(fileLink);

             fileLink.click();
          })
      }
    }
  }
</script>

