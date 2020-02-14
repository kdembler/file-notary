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
        <tr v-for="item in items" :key="item.name">
          <td>{{ item.name }}</td>
          <td :class="{ 'red--text': filesStatuses[item.name] === 2 }">
            <hash-table-cell :hash="item.localHash" />
          </td>
          <td>
            <v-icon v-if="filesStatuses[item.name] === 0" color="green">mdi-check</v-icon>
            <v-progress-circular
              v-else-if="filesStatuses[item.name] === 1"
              indeterminate
              color="primary"
              :size="30"
              :width="2"
            />
            <v-icon v-else-if="filesStatuses[item.name] === 2" color="red ">mdi-alert-circle-outline</v-icon>
          </td>
          <td>
            <v-btn text @click="onDownloadClick(item)">
              {{ filesStatuses[item.name] === 2 ? 'Download anyway' : 'Download' }}
            </v-btn>
          </td>
        </tr>
      </tbody>
    </template>
  </v-data-table>
</template>
<script lang="ts">
import Vue from 'vue'
import Web3 from 'web3'
import axios from 'axios'
import HashTableCell from '@/components/HashTableCell.vue'
import FileNotary from './fileNotary.json'
import { File } from '../types/file'
import { getFileHash } from '../utils'

enum FileStatus {
  Ok,
  Pending,
  Invalid,
}

export default Vue.extend({
  components: {
    HashTableCell,
  },

  data() {
    return {
      headers: [
        { text: 'Filename', value: 'name', align: 'left' },
        { text: 'Local hash', value: 'localHash' },
        { text: 'Status', value: 'status' },
        { text: '', value: 'actions' },
      ],
      intervalId: null as number | null,
    }
  },

  created() {
    // TODO: consider using events instead of polling
    const web3 = new Web3('wss://kovan.infura.io/ws/v3/d94c6d05fdac485d8e50a77ff1ff6793')
    const notary = new web3.eth.Contract(FileNotary.abi, FileNotary.address)
    this.intervalId = setInterval(async () => {
      this.files
        .filter(file => !file.blockchainHash)
        .forEach(async file => {
          const hash = await notary.methods.getFileHash(file.name).call()
          if (hash !== '0x0000000000000000000000000000000000000000000000000000000000000000') {
            this.$store.commit('updateFile', { name: file.name, fields: { blockchainHash: hash } })
          }
        })
    }, 2000)
  },

  beforeDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId)
    }
  },

  computed: {
    files(): File[] {
      return this.$store.state.files
    },

    filesStatuses(): { [name: string]: FileStatus } {
      return this.files.reduce(
        (acc, file) => {
          let status = FileStatus.Ok
          if (!file.blockchainHash) {
            status = FileStatus.Pending
          } else if (file.blockchainHash !== file.localHash) {
            status = FileStatus.Invalid
          }
          acc[file.name] = status
          return acc
        },
        {} as { [name: string]: FileStatus }
      )
    },
  },

  methods: {
    async onDownloadClick(file: File) {
      if (this.filesStatuses[file.name] === FileStatus.Invalid) {
        this.saveFile(file)
        return
      }
      try {
        const urlResponse = await axios.get('http://localhost:5000/download-url', { params: { file: file.name } })
        const { url } = urlResponse.data

        const fileResponse = await axios.get(url, { responseType: 'blob' })
        const fileBlob = new Blob([fileResponse.data])
        const objectUrl = URL.createObjectURL(fileBlob)
        console.log(objectUrl)
        const hash = await getFileHash(fileBlob)
        const valid = hash === file.blockchainHash

        this.$store.commit('updateFile', { name: file.name, fields: { objectUrl, localHash: hash } })

        if (valid) {
          this.saveFile(file)
        }
      } catch (error) {
        console.error(error)
      }
    },

    saveFile(file: File) {
      const a = document.createElement('a')
      a.href = file.objectUrl as string
      a.download = file.name
      document.body.appendChild(a)
      a.click()
    },
  },
})
</script>
<style lang="scss" scoped>
.table {
  min-width: 602px;
}
</style>
