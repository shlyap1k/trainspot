<template>
  <v-card class="" min-width="480">
    <v-card-title v-if="role === 'admin'">
      Показать отчет о работе зала
    </v-card-title>
    <v-card-title v-else>
      Показать отчет
    </v-card-title>
    <v-card-subtitle>
      Сформировать отчёт
    </v-card-subtitle>
    <v-card-actions>
      <v-layout row wrap>
        <v-spacer></v-spacer>
        <v-flex v-if="role === 'admin'">
          <v-menu
            ref="menu1"
            v-model="menu1"
            :close-on-content-click="false"
            :nudge-right="40"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            max-width="290px"
            min-width="290px"
          >
            <template v-slot:activator="{ on }">
              <v-text-field
                v-model="date1"
                label="начиная с"
                hint="YYYY/MM/DD формат"
                persistent-hint
                readonly
                @blur="date = parseDate(dateFormatted)"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker v-model="date1" no-title @input="menu1 = false"></v-date-picker>
          </v-menu>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex v-if="role === 'admin'">
          <v-menu
            v-model="menu2"
            :close-on-content-click="false"
            :nudge-right="40"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            max-width="290px"
            min-width="290px"
          >
            <template v-slot:activator="{ on }">
              <v-text-field
                v-model="date2"
                label="и до"
                hint="YYYY/MM/DD формат"
                persistent-hint
                readonly
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker v-model="date2" no-title @input="menu2 = false"></v-date-picker>
          </v-menu>
        </v-flex>
        <v-spacer></v-spacer>
        <v-btn @click="getpdf()">
          получить файл
        </v-btn>
      </v-layout>
      <v-spacer></v-spacer>
    </v-card-actions>
    .
    <v-spacer></v-spacer>
    <iframe v-if="pdfUrl" :src="pdfUrl" style="width:100%;height:800px;"></iframe>
  </v-card>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import {mapGetters} from "vuex";
  export default {
    name: "GetPdfReport",
    data() {
      return {
        file: null,
        datepicker1: false,
        date1: null,
        date2: null,
        pdfUrl: '',
        params: {},
        dateFormatted: this.formatDate(new Date().toISOString().substr(0, 10)),
        menu1: false,
        menu2: false
      }
    },
    watch: {
      date (val) {
        this.dateFormatted = this.formatDate(this.date)
      }
    },
    methods: {
      formatDate (date) {
        if (!date) return null

        const [year, month, day] = date.split('-')
        return `${month}/${day}/${year}`
      },
      parseDate (date) {
        if (!date) return null

        const [month, day, year] = date.split('/')
        return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
      },
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
      }),
      computedDateFormatted () {
        return this.formatDate(this.date)
      }
    }
  }
</script>

