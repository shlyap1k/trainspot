<template>
  <v-card>
    <v-card-title>
      Организационная диаграмма
    </v-card-title>
    <v-card-text align="center">
        <GChart
          :settings="{packages: ['orgchart']}"
          type="OrgChart"
          :data="chartOrgData"
          :options="chartOrgOptions"
        />
    </v-card-text>
  </v-card>
</template>

<script>
  import { GChart } from 'vue-google-charts/legacy'
  export default {
    name: "PlansHierarchyDiagram",
    components: {
      GChart
    },
    props: {
      plan_types: {
        type: Array,
        required: true
      },
      plans: {
        type: Array,
        required: true
      }
    },
    computed: {
      chartOrgData: function () {
        const data = [
          ['Name', 'Manager', 'Tooltip'],
          ['Ассортимент', null, 'Типы абонементов'],
        ]
        this.plan_types.forEach(value => {
          data.push([value, 'Ассортимент', value])
        })

        this.plans.forEach(value => {
          data.push([value.name, value.plan_type.name, value.name])
        })
        return data
      }
    },
    data() {
      return {
        chartOrgOptions: {
          title: 'Assortment Structure',
          allowHtml: true,
          height: 300
        }
      }
    }
  }
</script>

