import axios, { AxiosInstance } from 'axios'
import { AuthService } from '@/services/auth'
import { RootStore } from '@/store'
import { fileDetailsUrl, filesUrl } from '@/urls'
import { FileInfo } from '@/types/fileInfo'
import Web3Service from '@/services/web3'
import { getFileHash } from '@/utils/hash'

export default class NotaryService {
  client: AxiosInstance

  constructor(authService: AuthService, private store: RootStore, private web3Service: Web3Service) {
    this.client = axios.create()
    this.client.interceptors.request.use(async config => {
      const token = authService.getToken()
      if (!token) {
        throw Error('No token available for Notary request')
      }

      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`,
      }
      return config
    })
  }

  async fetchFiles() {
    const response = await this.client.get<FileInfo[]>(filesUrl)
    const files = response.data

    files.forEach(file =>
      this.web3Service.getFileBlockchainHash(file.id).then(hash => {
        this.store.commit('updateFile', { id: file.id, fields: { blockchainHash: hash } })
      })
    )

    this.store.commit('setFiles', files)
  }

  async uploadFile(file: File, hash: string) {
    const formData = new FormData()
    formData.append('file', file, file.name)
    const response = await this.client.post<FileInfo>(filesUrl, formData)
    const newFile: FileInfo = {
      ...response.data,
      localHash: hash,
    }

    this.web3Service.getFileBlockchainHash(newFile.id).then(hash => {
      this.store.commit('updateFile', { id: newFile.id, fields: { blockchainHash: hash } })
    })

    this.store.commit('addFile', newFile)
  }

  async downloadFile(fileId: string) {
    type DownloadResponse = FileInfo & { download_url: string }
    const urlResponse = await this.client.get<DownloadResponse>(fileDetailsUrl(fileId))
    const { download_url: url } = urlResponse.data

    const fileResponse = await axios.get(url, { responseType: 'blob' })
    const fileBlob = new Blob([fileResponse.data])
    const objectUrl = URL.createObjectURL(fileBlob)
    const hash = await getFileHash(fileBlob)
    this.store.commit('updateFile', { id: fileId, fields: { objectUrl, localHash: hash } })
    return objectUrl
  }
}
