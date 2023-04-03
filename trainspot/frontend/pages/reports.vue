<template>
  <div>
    <v-row v-if="role==='admin'">
      <v-col cols="4">
        <v-container>
          <v-layout flex align-left justify-center>
            <v-flex xs4 sm12 elevation-4>
              <v-card>
                <v-card-title>
                  Количество заказов
                </v-card-title>
                <v-card-text>
                  <purchases-count-plot/>
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-col>
      <v-col cols="4">
        <v-container>
          <v-layout flex align-left justify-center>
            <v-flex xs4 sm10 elevation-4>
              <v-card>
                <v-card-title>
                  Сумма заказов
                </v-card-title>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-col>
      <v-col cols="4">
        <v-container>
          <v-layout flex align-left justify-center>
            <v-flex xs4 sm10 elevation-4>
              <v-card>
                <v-card-title>
                  Новые пользователи
                </v-card-title>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-col>
    </v-row>
    <v-row v-if="role==='admin'">
      <v-container>
        <v-layout flex align-left justify-center>
          <v-flex xs4 sm10 elevation-4>
            <statistical-dynamics/>
          </v-flex>
        </v-layout>
      </v-container>
    </v-row>
    <v-row v-if="role==='admin'">
      <v-container>
        <v-layout flex align-left justify-center>
          <v-flex xs4 sm10 elevation-4>
            <profit-plot/>
          </v-flex>
        </v-layout>
      </v-container>
    </v-row>
    <v-row v-if="role==='client'">
      <v-container>
        <v-layout flex align-left justify-center>
          <v-flex xs4 sm10 elevation-4>
            <expenses-by-categories-pie/>
          </v-flex>
        </v-layout>
      </v-container>
    </v-row>
    <v-row>
      <v-container>
        <v-layout flex align-right justify-center>
          <v-flex xs6 sm10 elevation-4>
            <get-pdf-report/>
          </v-flex>
        </v-layout>
      </v-container>
    </v-row>
  </div>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import {mapGetters} from "vuex";
  import GetPdfReport from "@/components/GetPdfReport.vue";
  import ProfitPlot from "@/components/ProfitPlot.vue";
  import ExpensesByCategoriesPie from "@/components/ExpensesByCategoriesPie.vue";
  import StatisticalDynamics from "@/components/StatisticalDynamics.vue";
  import PurchasesCountPlot from "@/components/PurchasesCountPlot.vue";

  export default {
    name: "reports",
    components: {
      GetPdfReport,
      ProfitPlot,
      ExpensesByCategoriesPie,
      StatisticalDynamics,
      PurchasesCountPlot
    },
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

