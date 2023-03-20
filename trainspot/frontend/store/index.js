// import Vuex from 'vuex'
// import createPersistedState from "vuex-persistedstate"
//
//
// new Vuex.Store({
//   plugins: [
//     createPersistedState()
//   ],
//   state: () => ({
//     counter: 0
//   }),
//   mutations: {
//     increment(state) {
//       state.counter++
//     }
//   },
//   modules: {
//     todos: {
//       namespaced: true,
//       state: () => ({
//         list: []
//       }),
//       mutations: {
//         add(state, { text }) {
//           state.list.push({
//             text,
//             done: false
//           })
//         },
//         remove(state, { todo }) {
//           state.list.splice(state.list.indexOf(todo), 1)
//         },
//         toggle(state, { todo }) {
//           todo.done = !todo.done
//         }
//       }
//     },
//     fruits: {
//       namespaced: true,
//       state: () => ({
//         fruits: [],
//       }),
//       mutations: {
//         addFruit(state, fruit) {
//           state.fruits.push(fruit)
//         },
//         removeFruit(state, fruitId) {
//           state.fruits = state.fruits.filter((fruit) => fruit.id !== fruitId)
//         },
//       },
//       actions: {
//         addFruit(context, fruit) {
//           // const slicedFruit = fruit
//           context.commit(fruit)
//         },
//       },
//       getters: {
//         getApples: (state) => {
//           return state.fruits.filter((fruit) => fruit.type === 'Apple')
//         },
//       }
//     }
//   }
// })

// store/index.js

export const state = () => {}

export const mutations = {}

export const actions = {}

export const getters = {}
