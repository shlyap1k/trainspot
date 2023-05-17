<template>
  <v-container class="grey lighten-5">
    <v-row>
      <v-col cols="6">
        <profit-and-predicted-profit-diagram :raw-data="rawData" :plans="plans" v-if="rawData.length > 1 && plans.length > 1"/>
      </v-col>
      <v-col cols="6">
        <sells-and-profit-bubble-diagram :raw-data="rawData"/>
      </v-col>
    </v-row>
    <v-row>
      <v-col sm="12">
        <purchases-calendar :raw-data="rawData" v-if="rawData"/>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <plans-hierarchy-diagram :plans="plans" :plan_types="plan_types"/>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <users-count-map :cities="cities" :users="users" v-if="cities"/>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <sankey-diagram :raw-data="rawData" :plans="plans" :users="users" v-if="users"/>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <sells-timeline :plans="plans" :raw-data="rawData" v-if="plans"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import apiClient from '@/src/apiClient'
  import UsersCountMap from "@/components/diagrams/UsersCountMap.vue";
  import SellsTimeline from "@/components/diagrams/SellsTimeline.vue";
  import SankeyDiagram from "@/components/diagrams/SankeyDiagram.vue";
  import PlansHierarchyDiagram from "@/components/diagrams/PlansHierarchyDiagram.vue";
  import PurchasesCalendar from "@/components/diagrams/PurchasesCalendar.vue";
  import SellsAndProfitBubbleDiagram from "@/components/diagrams/SellsAndProfitBubbleDiagram.vue";
  import ProfitAndPredictedProfitDiagram from "@/components/diagrams/ProfitAndPredictedProfitDiagram.vue";
  export default {
    components: {
      UsersCountMap,
      SellsTimeline,
      SankeyDiagram,
      PlansHierarchyDiagram,
      PurchasesCalendar,
      SellsAndProfitBubbleDiagram,
      ProfitAndPredictedProfitDiagram
    },
    name: "diagrams",
    mounted() {
      apiClient
        .get('financialrecords/')
        .then(response => {
          this.rawData=JSON.parse(JSON.stringify(response.data))
        })

      apiClient
        .get('plans/')
        .then(response => {
          this.plans=response.data
          this.get_plan_types()
        })

      apiClient
        .get('users/')
        .then(response => {
          this.users = response.data.results
        })

      apiClient
        .get('cities/')
        .then(response => {
          this.cities = response.data.results
      })
    },
    methods: {
      get_plan_types() {
        this.plans.map(element => {
          return this.plan_types.push(element.plan_type.name)
        });
        this.plan_types = this.plan_types.filter((value, index) => this.plan_types.indexOf(value) === index)
      },
    },
    data() {
      return {
        cities: [],
        users: [],
        rawData: [],
        plans: [],
        plan_types: [],
       }
     }
  }
</script>
