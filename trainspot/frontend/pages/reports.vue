<template>
<div>
  <v-container>
    <v-layout flex align-center justify-center>
      <v-flex xs4 sm5 elevation-4>
        <v-card class="">
          <v-card-title>
            Показать отчет о работе зала
          </v-card-title>
          <v-card-subtitle>
            Сформировать отчёт
          </v-card-subtitle>
          <v-card-actions v-if="role === 'admin'">
            <v-row>
              <v-col>Начиная с {{date1}}
                <v-date-picker v-model="date1" :landscape="landscape" :reactive="reactive"></v-date-picker>
              </v-col>
              <v-spacer></v-spacer>
              <v-col>И до {{date2}}
                <v-date-picker v-model="date2" :landscape="landscape" :reactive="reactive"></v-date-picker>
              </v-col>
            </v-row>
          </v-card-actions>
          <v-btn @click="getpdf()">
            получить файл
          </v-btn>
          <iframe v-if="pdfUrl" :src="pdfUrl" style="width:100%;height:800px;"></iframe>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</div>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import axios from "axios";
  import {mapGetters} from "vuex";

  export default {
    name: "reports",
    data() {
      return {
        file: null,
        date1: null,
        date2: null,
        pdfUrl: '',
        params: {},
      }
    },
    methods: {
      getpdf() {
        if (this.date1) {
          if (this.date2) {
            this.params = {
              start: this.date1,
              end: this.date2
            }

          }
        }
        apiClient.get("financialrecords/1/download/", {
          responseType: "arraybuffer",
          params: this.params,
          headers: {
            accept: 'application/pdf',
            // params: this.params
          }
        }).then(response => {
          const blob = new Blob([response.data], {type: 'application/pdf'});
          this.pdfUrl = URL.createObjectURL(blob);
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "file.pdf");
          document.body.appendChild(link);
          // link.click();
        });
      }
    },
    computed: {
      ...mapGetters({
        role: 'user/getRole'
      })
    }
  }
</script>

