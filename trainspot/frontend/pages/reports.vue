<template>
  <div>
    <h1>
      Статистика
    </h1>
    <v-row>
      <v-col v-if="role==='admin'" cols="12">
        <v-row>
          <v-col cols="12" sm="6">
            <v-card>
              <v-card-title>Динамика количества продаж</v-card-title>
              <v-card-text>
                На графике отчетливо прослеживается изменение количества продаж в течении года.
                В зимние и весенние месяцы наблюдается наибольший спрос, летом и осенью количество
                продаж значительно меньше
                <purchases-count-plot/>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6">
            <v-card>
              <v-card-title>Динамика регистрации новых пользователей</v-card-title>
              <v-card-text>
                В течение месяца не было существенных отклонений в числе новых регистраций,
                за исключением резкого всплеска регистраций 14 марта, что может указывать на стабильность интереса.
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
                <v-list>
                  <v-list-item>
                    Наиболее популярным типом занятий являются самостоятельные занятия и групповые занятия.
                    Оба типа занятий имеют высокие продажи на протяжении всего года.
                  </v-list-item>
                  <v-list-item>
                    Персональные занятия с тренером имеют низкие продажи в течение года и не пользуются большой популярностью у клиентов.
                  </v-list-item>
                  <v-list-item>
                    Единоборства также имеют низкие продажи, но они достигают пика в апреле месяце.
                  </v-list-item>
                  <v-list-item>
                    Можно заметить сезонные колебания продаж: в начале года (январь-февраль) продажи обычно высокие, затем они падают к марту, затем немного восстанавливаются в апреле, затем снова снижаются до лета, после чего немного растут в августе-сентябре и снова падают к концу года.
                  </v-list-item>
                  <v-list-item>
                    В целом, продажи абонементов по всем типам занятий низкие в марте 2023 года, когда были проданы только самостоятельные занятия.
                  </v-list-item>
                </v-list>
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
  import GetPdfReport from "@/components/reports/GetPdfReport.vue";
  import ProfitPlot from "@/components/reports/Plots/ProfitPlot.vue";
  import ExpensesByCategoriesPie from "@/components/reports/Plots/ExpensesByCategoriesPie.vue";
  import StatisticalDynamics from "@/components/reports/Statistics/StatisticalDynamics.vue";
  import PurchasesCountPlot from "@/components/reports/Plots/PurchasesCountPlot.vue";
  import NewUsersPlot from "@/components/reports/Plots/NewUsersPlot.vue";
  import StatisticsByTypes from "@/components/reports/Plots/StatisticsByTypes.vue";

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

