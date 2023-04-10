<template>
  <v-row>
    <v-dialog
      v-model="dialog"
      persistent
      width="1024"
    >
      <template v-slot:activator="{ props }">
        <v-btn
          v-bind="props"
          icon
          @click="dialog=true"
        >
          <v-icon>mdi-cart</v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-row>
          <v-col cols="10">
            <v-card-title>
              <span class="text-h5">Покупка абонемента</span>
            </v-card-title>
          </v-col>
          <v-spacer></v-spacer>
          <v-col>
            <v-btn
              color="blue-darken-1"
              icon
              @click="dialog = false"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <v-card-text>
          <v-data-table
            :headers="headers"
            :items="plans"
            :search="search"
            item-class="clickable-row"
            class="elevation-1"
          >
            <template v-slot:body="{ items }">
              <tbody>
                <tr v-for="(item, index) in items" :key="index"  @click="handleRowClick(item)">
                  <td>{{ item.name }}</td>
                  <td>{{ item.description }}</td>
                  <td>{{ item.price }}</td>
                  <td>{{ item.duration_days }}</td>
                  <td>{{ item.visits_count }}</td>
                  <td>{{ item.plan_type.name }}</td>
                </tr>
              </tbody>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
  import apiClient from "@/src/apiClient";
  import BuyPlanForm from "@/components/BuyPlanForm.vue";

  export default {
    name: "BuyPlan",
    components: {
      BuyPlanForm
    },
    data(){
      return {
        dialog: false,
        modalVisible: false,
        plans: [],
        selectedPlan: [],
        headers: [
          { text: "Название", value: "name" },
          { text: "Описание", value: "description" },
          { text: "Цена", value: "price" },
          { text: "Длительность (дни)", value: "duration_days" },
          { text: "Посещений", value: "visits_count" },
          { text: "Тип", value: "plan_type.name" },
        ],
        search: "",
      }
    },
    created() {
      this.fetchPlans();
    },
    methods: {
      fetchPlans() {
        apiClient.get("plans/")
          .then((response) => response.data)
          .then((data) => {
            this.plans = data;
          })
          .catch((error) => console.log(error));
      },
      handleRowClick(item) {
        console.log(item.name)
        this.modalVisible = true
        this.selectedPlan = item
      }
    },
  }
</script>
