<!--<template>-->
<!--  <div>-->
<!--    <v-row v-if="role==='admin'" >-->
<!--      <v-col cols="5">-->
<!--        <v-container>-->
<!--          <v-layout>-->
<!--            <v-flex xs4 sm12 elevation-4>-->
<!--              <v-card>-->
<!--                <v-card-title>-->
<!--                  Динамика количества продаж-->
<!--                </v-card-title>-->
<!--                <v-card-text>-->
<!--                  <purchases-count-plot/>-->
<!--                </v-card-text>-->
<!--              </v-card>-->
<!--            </v-flex>-->
<!--          </v-layout>-->
<!--        </v-container>-->
<!--      </v-col>-->
<!--      <v-col cols="5">-->
<!--        <v-container>-->
<!--          <v-layout>-->
<!--            <v-flex xs4 sm12 elevation-4>-->
<!--              <v-card>-->
<!--                <v-card-title>-->
<!--                  Динамика регистрации новых пользователей-->
<!--                </v-card-title>-->
<!--                <v-card-text>-->
<!--                  <new-users-plot/>-->
<!--                </v-card-text>-->
<!--              </v-card>-->
<!--            </v-flex>-->
<!--          </v-layout>-->
<!--        </v-container>-->
<!--      </v-col>-->
<!--    </v-row>-->
<!--    <v-row v-if="role==='admin'">-->
<!--      <v-col>-->
<!--        <v-container>-->
<!--          <v-layout flex align-left justify-center>-->
<!--            <v-flex xs4 sm10 elevation-4>-->
<!--              <v-card>-->
<!--                <v-card-title>-->
<!--                  Динамика покупок отдельных типов абонементов-->
<!--                </v-card-title>-->
<!--                <statistics-by-types/>-->
<!--              </v-card>-->
<!--            </v-flex>-->
<!--          </v-layout>-->
<!--        </v-container>-->
<!--      </v-col>-->
<!--    </v-row>-->
<!--    <v-row v-if="role==='admin'">-->
<!--      <v-container>-->
<!--        <v-layout flex align-left justify-center>-->
<!--          <v-flex xs4 sm10 elevation-4>-->
<!--            <statistical-dynamics/>-->
<!--          </v-flex>-->
<!--        </v-layout>-->
<!--      </v-container>-->
<!--    </v-row>-->
<!--    <v-row v-if="role==='admin'">-->
<!--      <v-container>-->
<!--        <v-layout flex align-left justify-center>-->
<!--          <v-flex xs4 sm10 elevation-4>-->
<!--            <profit-plot/>-->
<!--          </v-flex>-->
<!--        </v-layout>-->
<!--      </v-container>-->
<!--    </v-row>-->
<!--    <v-row v-if="role==='client'">-->
<!--      <v-container>-->
<!--        <v-layout flex align-left justify-center>-->
<!--          <v-flex xs4 sm10 elevation-4>-->
<!--            <expenses-by-categories-pie/>-->
<!--          </v-flex>-->
<!--        </v-layout>-->
<!--      </v-container>-->
<!--    </v-row>-->
<!--    <v-row>-->
<!--      <v-container>-->
<!--        <v-layout flex align-right justify-center>-->
<!--          <v-flex xs6 sm10 elevation-4>-->
<!--            <get-pdf-report/>-->
<!--          </v-flex>-->
<!--        </v-layout>-->
<!--      </v-container>-->
<!--    </v-row>-->
<!--  </div>-->
<!--</template>-->
<template>
  <div>
    <v-row>
      <v-col v-if="role==='admin'" cols="12">
        <v-row>
          <v-col cols="12" sm="6">
            <v-card>
              <v-card-title>Динамика количества продаж</v-card-title>
              <v-card-text>
                <purchases-count-plot/>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6">
            <v-card>
              <v-card-title>Динамика регистрации новых пользователей</v-card-title>
              <v-card-text>
                <new-users-plot/>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-card>
              <v-card-title>Динамика покупок отдельных типов абонементов</v-card-title>
              <v-card-text>
                <statistics-by-types/>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <statistical-dynamics/>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <profit-plot/>
          </v-col>
        </v-row>
      </v-col>
      <v-col v-else cols="12">
        <expenses-by-categories-pie/>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <get-pdf-report/>
      </v-col>
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
  import NewUsersPlot from "@/components/NewUsersPlot.vue";
  import StatisticsByTypes from "@/components/StatisticsByTypes.vue";

  export default {
    name: "reports",
    components: {
      GetPdfReport,
      ProfitPlot,
      ExpensesByCategoriesPie,
      StatisticalDynamics,
      PurchasesCountPlot,
      NewUsersPlot,
      StatisticsByTypes
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

