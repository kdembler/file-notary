<template>
  <v-card min-width="500">
    <v-card-title>Register</v-card-title>
    <v-card-subtitle>Create new File Notary account</v-card-subtitle>
    <v-card-text class="text--black" v-if="registerDone">
      <p class="text-center">This is your new user code:</p>
      <h3 class="text-center display-1 font-weight-bold">{{ newUserCode }}</h3>
      <p class="text-center mb-0 mt-3">Please write it down. It will be required to log in later on.</p>
    </v-card-text>
    <v-card-actions class="pb-5">
      <v-btn :loading="registerInProgress" @click="clicked()" class="mx-auto px-5" color="primary" x-large>
        {{ registerDone ? 'Got it' : 'Register' }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Inject } from 'vue-property-decorator'
import { AuthService } from '@/services/auth'

@Component
export default class LoginView extends Vue {
  @Inject('authService') authService!: AuthService

  registerInProgress = false
  newUserCode = ''

  get registerDone() {
    return !!this.newUserCode
  }

  async clicked() {
    this.registerDone ? await this.$router.push('/') : await this.register()
  }

  async register() {
    this.registerInProgress = true
    this.newUserCode = await this.authService.register()
    this.registerInProgress = false
  }
}
</script>
