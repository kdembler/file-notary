<template>
  <v-card min-width="500">
    <v-card-title>Log in</v-card-title>
    <v-card-subtitle>Log in to your existing File Notary account</v-card-subtitle>
    <v-form @submit="logIn()">
      <v-card-text>
        <v-text-field class="user-field mx-5" label="User code" required solo v-model.trim="userCode" />
      </v-card-text>
      <v-card-actions class="pb-5">
        <v-btn
          :disabled="!userCodeValid"
          :loading="logInInProgress"
          @click="logIn()"
          class="mx-auto px-5"
          color="primary"
          x-large
        >
          Log in
        </v-btn>
      </v-card-actions>
    </v-form>
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

  userCode = ''
  logInInProgress = false

  get userCodeValid() {
    return this.userCode.length === 6
  }

  async logIn() {
    if (!this.userCodeValid) {
      return
    }
    this.logInInProgress = true
    await this.authService.logIn(this.userCode)
    await this.$router.push({ path: '/' })
    this.logInInProgress = false
  }
}
</script>

<style lang="scss">
.user-field input {
  font-size: 32px;
  max-height: none;
  text-align: center;
}
</style>
