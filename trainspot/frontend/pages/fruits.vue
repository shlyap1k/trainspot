<template>
  <v-card>
    <v-btn @click="addAppleFromComponent()">добавить яблоко</v-btn>
    <v-btn @click="addOrangeFromComponent()">добавить апельсин</v-btn>
    <v-btn @click="addFruitFromComponent()">добавить фрукт</v-btn>
    <v-btn
      :loading="loading[1]"
      :disabled="loading[1]"
      @click="load(1)"
    >
      Accept Terms
    </v-btn>
    <ul>
        <li v-for="fruit in fruits" :key="fruit.id">
            {{ fruit.name }} - {{ fruit.type }}
        </li>
    </ul>
    <ul>
      <p>яблоки:</p>
        <li v-for="fruit in apples" :key="fruit.id">
            {{ fruit.name }} - {{ fruit.type }}
        </li>
    </ul>
  </v-card>
</template>

<script>
export default {
  data () {
      return {
        loading: [],
      }
    },
  computed: {
    apples() {
        // return this.$store.state.fruits.getters.getApples()
      return this.$store.getters["fruits/getApples"]
    },
    fruits() {
        // return this.$store.state.fruits.getters.getApples()
      return this.$store.state.fruits.fruits
    },
  },
  methods: {
    addFruitFromComponent() {
        const newFruit = {
            name: 'Tasty Fruit',
            type: 'Fruit',
            id: 3,
        }

        // Используем dispatch чтобы вызвать экшен
        this.$store.dispatch('fruits/addFruit', newFruit)

        // Используем коммит чтобы вызвать мутацию
        this.$store.commit('fruits/addFruit', newFruit)
    },
    addAppleFromComponent() {
      const newFruit = {
          name: 'Big Apple',
          type: 'Apple',
          id: 3,
          }
          // Используем dispatch чтобы вызвать экшен
      this.$store.dispatch('fruits/addFruit', newFruit)

      // Используем коммит чтобы вызвать мутацию
      this.$store.commit('fruits/addFruit', newFruit)
    },
    addOrangeFromComponent() {
      const newFruit = {
          name: 'Orange Orange',
          type: 'Orange',
          id: 3,
        }
        // Используем dispatch чтобы вызвать экшен
      this.$store.dispatch('fruits/addFruit', newFruit)

      // Используем коммит чтобы вызвать мутацию
      this.$store.commit('fruits/addFruit', newFruit)
    },
    load (i) {
        this.loading[i] = true
        setTimeout(() => (this.loading[i] = false), 3000)
      },
    },
}
</script>

<style>
  .custom-loader {
    animation: loader 1s infinite;
    display: flex;
  }
  @-moz-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-webkit-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-o-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>
