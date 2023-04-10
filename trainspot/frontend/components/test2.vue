<template>
  <v-dialog v-model="modalVisible" v-if="selectedItem">
    <!-- Modal content goes here -->
    <div>{{ selectedItem.name }}</div>
    <div>{{ selectedItem.email }}</div>
    <div>{{ selectedItem.phone }}</div>
  </v-dialog>
</template>

<script>
export default {
  name: 'test2',
  props: {
    selectedItem: Object,
    modalVisible: Boolean,
  },
};
</script>
