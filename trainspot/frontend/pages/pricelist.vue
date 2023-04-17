<template>
  <v-card>
    <price-list-charts :plans="plans"/>
    <iframe :src="pdfUrl" style="width:100%;height:800px;"></iframe>
  </v-card>
</template>

<script>
import apiClient from "@/src/apiClient";
import PriceListCharts from "@/components/PriceListCharts.vue";

export default {
  data() {
    return {
      pdfUrl: "",
      plans: []
    }
  },
  components: {
    PriceListCharts
  },
  mounted() {
    this.downloadPdfFile();
    this.getPlans();
  },
  methods: {
    downloadPdfFile() {
      const headers = {
        'Accept': 'application/pdf',
        'Content-Type': 'application/json'
        // Другие необходимые заголовки
      };

      apiClient.get("plans/1/download/", {
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
    },
    getPlans() {
      apiClient
        .get("plans/")
        .then(response => {
          this.plans = response.data
        })

    }
  }
};
</script>
