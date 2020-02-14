<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <h2 class="mr-3">File Notary</h2>
        <v-btn text to="/upload" class="mr-2"><v-icon left>mdi-file-upload</v-icon>Upload file</v-btn>
        <v-btn text to="/files"><v-icon left>mdi-file-multiple</v-icon>Files list</v-btn>
      </div>
    </v-app-bar>

    <v-content>
      <div class="d-flex flex-column justify-center align-center">
        <router-view />
      </div>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({})
</script>

<style lang="scss"></style>
