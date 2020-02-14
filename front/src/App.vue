<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <h2 class="mr-3">File Notary</h2>
      <template v-if="userService.isLoggedIn">
        <v-btn text to="/upload" class="mr-2"><v-icon left>mdi-file-upload</v-icon>Upload file</v-btn>
        <v-btn text to="/files"><v-icon left>mdi-file-multiple</v-icon>Files list</v-btn>
        <v-menu offset-y>
          <template v-slot:activator="{ on }">
            <v-btn class="ml-auto" text v-on="on">
              <v-icon left>mdi-account-circle</v-icon> {{ userService.userCode }}
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="logOut">
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
      <template v-else>
        <v-btn class="mr-2" text to="/login"><v-icon left>mdi-account</v-icon>Log in</v-btn>
        <v-btn text to="/register"><v-icon left>mdi-account-plus</v-icon>Register</v-btn>
      </template>
    </v-app-bar>

    <v-content>
      <div class="d-flex justify-center pt-5">
        <router-view />
      </div>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'
import { UserService } from '@/services/user'
import Component from 'vue-class-component'
import { Inject } from 'vue-property-decorator'

@Component
export default class App extends Vue {
  @Inject('userService') private userService!: UserService

  async logOut() {
    this.userService.logOut()
    await this.$router.push('/login')
  }
}
</script>

<style lang="scss"></style>
