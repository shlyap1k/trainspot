<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="items"
      @click:row="showModal"
    >
      <template #item="{ item }">
        <tr>
          <td  @click="showModal(item)">{{ item.name }}</td>
          <td>{{ item.description }}</td>
          <td>{{ item }}</td>
        </tr>
      </template>
    </v-data-table>

    <test2
      :selectedItem="selectedItem"
      :modalVisible="modalVisible"
    />
  </div>
</template>

<script>
import test2 from "@/components/test2.vue";

export default {
  components: { test2 },
  data() {
    return {
      headers: [
        { text: 'Name', value: 'name' },
        { text: 'Email', value: 'email' },
        { text: 'Phone', value: 'phone' },
      ],
      items: [
        { name: 'John Doe', email: 'john@example.com', phone: '555-1234' },
        { name: 'Jane Smith', email: 'jane@example.com', phone: '555-5678' },
      ],
      modalVisible: false,
      selectedItem: [],
    };
  },
  methods: {
    showModal(item) {
      // Set the selected item data and open the modal
      this.selectedItem = item;
      this.modalVisible = true;
    },
  },
};
</script>
