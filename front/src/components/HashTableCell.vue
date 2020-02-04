<template>
  <div class="hash-cell d-flex justify-center">
    <v-fade-transition leave-absolute>
      <v-tooltip v-if="hash" bottom>
        <template v-slot:activator="{ on }">
          <div v-on="on" class="hash">
            <span>{{ hash }}</span>
          </div>
        </template>
        {{ hash }}
      </v-tooltip>
      <v-progress-circular v-else indeterminate color="primary" :size="30" :width="2" />
    </v-fade-transition>
  </div>
</template>
<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: {
    hash: {
      type: String,
      required: false,
      default: null,
    },
  },
})
</script>
<style lang="scss" scoped>
.hash-cell {
  width: 200px;
}

.hash {
  overflow-x: hidden;
  text-overflow: ellipsis;
}
</style>
