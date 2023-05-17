<template>
<v-simple-table>
      <thead>
        <tr>
          <th class="text-left">
            Дата
          </th>
          <th class="text-left">
            <katex-element expression="y_t"/>
          </th>
          <th class="text-left">
            <katex-element expression="x"/>
          </th>
          <th class="text-left">
            <katex-element expression="y_tx"/>
          </th>
          <th class="text-left">
            <katex-element expression="x^2"/>
          </th>
          <th class="text-left">
            <katex-element expression="y_tx^2"/>
          </th>
          <th class="text-left">
            <katex-element expression="x^4"/>
          </th>
          <th class="text-left">
            <katex-element expression="ln(y_t)"/>
          </th>
          <th class="text-left">
            <katex-element expression="ln(y_t)x"/>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data.slice(1)">
          <td>
            {{ item[0] }}
          </td>
          <td>
            {{ item[1] }}
          </td>
          <td>
            {{ data.indexOf(item) - Math.floor(data.length/2) }}
          </td>
          <td>
            {{ item[1] * (data.indexOf(item) - Math.floor(data.length/2)) }}
          </td>
          <td>
            {{ (data.indexOf(item) - Math.floor(data.length/2)) * (data.indexOf(item) - Math.floor(data.length/2)) }}
          </td>
          <td>
            {{ item[1] * ((data.indexOf(item) - Math.floor(data.length/2)) * (data.indexOf(item) - Math.floor(data.length/2))) }}
          </td>
          <td>
            {{ (data.indexOf(item) - Math.floor(data.length/2)) * (data.indexOf(item) - Math.floor(data.length/2)) * (data.indexOf(item) - Math.floor(data.length/2)) * (data.indexOf(item) - Math.floor(data.length/2)) }}
          </td>
          <td v-if="Math.log(item[1]) === -Infinity">
            <katex-element expression="-\infin"/>
          </td>
          <td v-else-if="Math.log(item[1]) === Infinity">
            <katex-element expression="\infin"/>
          </td>
          <td v-else>
            {{ Math.log(item[1]).toFixed(2) }}
          </td>
          <td v-if="(Math.log(item[1]) *  (data.indexOf(item) - Math.floor(data.length/2))) === -Infinity">
            <katex-element expression="-\infin"/>
          </td>
          <td v-else-if="(Math.log(item[1]) *  (data.indexOf(item) - Math.floor(data.length/2))) === Infinity">
            <katex-element expression="\infin"/>
          </td>
          <td v-else>
            {{ (Math.log(item[1]) *  (data.indexOf(item) - Math.floor(data.length/2))).toFixed(2) }}
          </td>

        </tr>
        <tr>
          <td>
            <katex-element expression="\sum_{}"/>
          </td>
          <td>
            {{data.slice(1).map(row=>row[1]).reduce((partialSum, a) => partialSum + a, 0)}}
          </td>
          <td>
          </td>
          <td>
<!--            y * x-->
            {{ data.slice(1).reduce((acc, curr, idx) => {
                  const index = (idx+1) - Math.floor((data.length-1) / 2);
                  const element = curr[1];
                  return acc + (element * index);
                }, 0) }}
          </td>
          <td>
<!--            x^2-->
            {{ data.slice(1).reduce((acc, curr, idx) => {
                  const index = (idx+1) - Math.floor((data.length-1) / 2);
                  return acc + (index * index);
                }, 0) }}
          </td>
          <td>
<!--            y*x^2-->
            {{ data.slice(1).reduce((acc, curr, idx) => {
                  const index = (idx+1) - Math.floor((data.length-1) / 2);
                  const element = curr[1];
                  return acc + (element * index * index);
                }, 0) }}
          </td>
          <td>
<!--            x^4-->
            {{ data.slice(1).reduce((acc, curr, idx) => {
                  const index = (idx+1) - Math.floor((data.length-1) / 2);
                  return acc + (index * index * index * index);
                }, 0) }}
          </td>
          <td>
<!--            ln(y)-->
            {{data.slice(1).map(row=>row[1]).reduce((partialSum, a) => partialSum + (Math.log(a) === -Infinity ? 0 : Math.log(a)), 0).toFixed(2)}}
          </td>
          <td>
<!--            ln(y)*x-->
            {{ data.slice(1).reduce((acc, curr, idx) => {
                  const index = (idx+1) - Math.floor((data.length-1) / 2);
                  let element = Number(Math.log(curr[1]).toFixed(2));
                  if (element === -Infinity) {
                    element = 0
                  }
                  return acc + (element * index);
                }, 0).toFixed(2) }}
          </td>
        </tr>
      </tbody>
    </v-simple-table>
</template>

<script>
  export default {
    name: "ModelsParamTable",
    props: {
      data: {
        type: Array,
        required: true
      }
    }
  }
</script>
