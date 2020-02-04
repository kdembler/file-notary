<template>
  <v-card class="mt-5" minWidth="500">
    <v-container>
      <v-row>
        <v-col>
          <h1>Uploader</h1>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <input class="d-none" ref="fileInput" type="file" value="Select file" @change="onFileChange($event)" />
          <v-btn @click="onSelectFileClick()" :diabled="uploadInProgress">Select file</v-btn>
        </v-col>
        <template v-if="fileToUpload">
          <v-col cols="12">
            <span>Selected file: {{ fileToUpload.name }}</span>
          </v-col>
        </template>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-btn @click="uploadFile()" :disabled="!fileToUpload" :loading="uploadInProgress">Upload file</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { createFile } from '../types/file'
import { getFileHash } from '@/utils'

export default Vue.extend({
  data() {
    return {
      fileToUpload: null as File | null,
      uploadInProgress: false,
      uploadFinished: false,
    }
  },

  methods: {
    onSelectFileClick() {
      this.$refs.fileInput.click()
    },

    onFileChange(event: Event) {
      if (!event.target) {
        return
      }
      const files = (event.target as any).files as FileList
      if (!files || files.length < 1) {
        return
      }
      this.fileToUpload = files[0]
    },

    async uploadFile() {
      if (!this.fileToUpload) {
        return
      }

      this.uploadInProgress = true
      this.$store.commit('addFile', createFile(this.fileToUpload.name))

      this.setFileHash()

      const formData = new FormData()
      formData.append('file', this.fileToUpload, this.fileToUpload.name)
      try {
        const response = await axios.post('http://localhost:5000/upload', formData)
        this.$store.commit('updateFile', {
          name: this.fileToUpload.name,
          // TODO: verify server hash is the same as local one
          // TODO: get rid of server hash
          fields: { serverHash: response.data.file_hash },
        })

        this.uploadInProgress = false
      } catch (error) {
        console.error(error)
      }
    },

    async setFileHash() {
      if (!this.fileToUpload) {
        return
      }

      const hash = await getFileHash(this.fileToUpload)

      this.$store.commit('updateFile', {
        name: this.fileToUpload.name,
        fields: { localHash: hash },
      })
    },
  },
})
</script>

<style lang="scss" scoped></style>
