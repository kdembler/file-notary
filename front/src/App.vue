<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <h2>File Notary</h2>
      </div>
    </v-app-bar>

    <v-content>
      <div class="d-flex flex-column justify-center align-center">
        <uploader />
        <uploads-list class="mt-5 elevation-4" />
      </div>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'
import Uploader from '@/components/Uploader.vue'
import UploadsList from '@/components/UploadsList.vue'

export default Vue.extend({
  components: {
    Uploader,
    UploadsList,
  },
})
</script>

<style lang="scss">
</style>
