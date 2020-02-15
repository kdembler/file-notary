<template>
  <v-card minWidth="500" max-width="500">
    <v-card-title>File upload</v-card-title>
    <v-card-subtitle>Select files to upload and notarize</v-card-subtitle>
    <v-card-text>
      <v-file-input show-size label="Select file" v-model="file" />
      <span class="text-center d-block mb-n5 status-text">{{ statusText }}</span>
    </v-card-text>
    <v-card-actions class="pb-5">
      <v-btn
        :disabled="!fileSelected"
        :loading="displayLoader"
        @click="uploadFile()"
        class="mx-auto px-5"
        color="primary"
        x-large
      >
        Upload
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { getFileHash } from '@/utils/hash'
import { Inject } from 'vue-property-decorator'
import NotaryService from '@/services/notary'

@Component
export default class UploadView extends Vue {
  @Inject('notaryService') notaryService!: NotaryService

  file = null as File | null
  status = 'INITIAL' as 'INITIAL' | 'HASHING' | 'UPLOADING'

  get fileSelected() {
    return !!this.file
  }

  get statusText() {
    switch (this.status) {
      case 'HASHING':
        return 'Status: Hashing...'
      case 'UPLOADING':
        return 'Status: Uploading...'
      default:
        return ''
    }
  }

  get displayLoader() {
    return this.status === 'HASHING' || this.status === 'UPLOADING'
  }

  async uploadFile() {
    if (!this.file) {
      return
    }

    this.status = 'HASHING'
    const hash = await getFileHash(this.file)

    this.status = 'UPLOADING'
    await this.notaryService.uploadFile(this.file, hash)

    await this.$router.push('/files')
  }
}
</script>

<style lang="scss" scoped>
.status-text {
  min-height: 22px;
}
</style>
