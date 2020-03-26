<template>
  <v-data-table
    class="table mt-5 elevation-4"
    :headers="headers"
    :items="files"
    :disable-pagination="true"
    :disable-sort="true"
  >
    <template v-slot:body="{ items }">
      <tbody>
        <tr v-for="item in items" :key="`${item.id}`">
          <td :class="{ 'red--text': filesStatuses[item.id] === 'ERROR' }">{{ item.name }}</td>
          <td align="center">
            <v-icon v-if="filesStatuses[item.id] === 'OK'" color="green">mdi-check</v-icon>
            <v-icon v-else-if="filesStatuses[item.id] === 'UNKNOWN'">mdi-help-circle</v-icon>
            <v-icon v-else-if="filesStatuses[item.id] === 'ERROR'" color="red">mdi-alert-circle-outline</v-icon>
          </td>
          <td>
            <v-btn text @click="onDownloadClick(item)" :loading="downloadsInProgress[item.id]">
              {{ filesStatuses[item.id] === 'ERROR' ? 'Download anyway' : 'Download' }}
            </v-btn>
          </td>
        </tr>
      </tbody>
    </template>
  </v-data-table>
</template>
<script lang="ts">
import Vue from 'vue'
import { FileInfo } from '@/types/fileInfo'
import Component from 'vue-class-component'
import NotaryService from '@/services/notary'
import { Inject } from 'vue-property-decorator'
import { saveFile } from '@/utils/file'

type FileStatus = 'UNKNOWN' | 'OK' | 'ERROR'

@Component
export default class FilesListView extends Vue {
  @Inject('notaryService') notaryService!: NotaryService

  downloadsInProgress = {} as Record<string, boolean>

  headers = [
    { text: 'File', value: 'name', align: 'left' },
    { text: 'Status', value: 'status' },
    { text: '', value: 'actions' },
  ]

  created() {
    this.notaryService.fetchFiles()
  }

  get files(): FileInfo[] {
    return this.$store.state.files
  }

  get filesStatuses(): Record<string, FileStatus> {
    return this.files.reduce(
      (acc, file) => {
        let status: FileStatus = 'OK'
        if (!file.blockchainHash || !file.localHash) {
          status = 'UNKNOWN'
        } else if (file.blockchainHash !== file.localHash) {
          status = 'ERROR'
        }
        acc[file.id] = status
        return acc
      },
      {} as Record<string, FileStatus>
    )
  }

  async onDownloadClick(file: FileInfo) {
    if (this.filesStatuses[file.id] === 'ERROR' && file.objectUrl) {
      saveFile(file)
    }
    this.$set(this.downloadsInProgress, file.id, true)
    const objectUrl = await this.notaryService.downloadFile(file.id)
    this.downloadsInProgress[file.id] = false

    if (this.filesStatuses[file.id] === 'OK') {
      const fileWithUrl = {
        ...file,
        objectUrl,
      }
      saveFile(fileWithUrl)
    }
  }
}
</script>
<style lang="scss" scoped>
.table {
  min-width: 602px;
}
</style>
