<template>
  <v-menu
    open-on-hover
    offset-y
    :close-on-content-click="false"
    rounded="xl"
  >
  <template v-slot:activator="{ on, attrs }">
    <div
      v-bind="attrs"
      v-on="on"
    >
      {{reactionsCount()}}
    </div>
  </template>

  <v-card
    rounded="xl"
  >
    <v-card-subtitle>
      Оценили:
    </v-card-subtitle>
    <v-card-text>
      <v-list>
        <div v-for="reaction in reactions">
          <div v-if="reaction.type===reactionType">
            <v-list-item>
              <v-card outlined>
                <v-card-title>
                  {{reaction.author.first_name + ' ' + reaction.author.last_name}}
                </v-card-title>
                <v-card-subtitle>
                  {{'@' + reaction.author.username}}
                </v-card-subtitle>
              </v-card>
            </v-list-item>
          </div>
        </div>
      </v-list>
    </v-card-text>
  </v-card>
  </v-menu>
</template>

<script>
  export default {
    name: "ReactionsList",
    props: {
      reactions: {
        type: Array,
        required: true
      },
      reactionType: {
        type: String,
        required: true
      }
    },
    methods: {
      reactionsCount() {
        if (this.reactions) {
          return this.reactions.reduce((total, x) => total + (x.type === this.reactionType), 0)
        }
      }
    },
  }
</script>

<style scoped>

</style>
