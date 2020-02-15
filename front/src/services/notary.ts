import axios, { AxiosInstance } from 'axios'
import { AuthService } from '@/services/auth'
import { RootStore } from '@/store'
import { filesUrl } from '@/urls'
import { FileInfo } from '@/types/fileInfo'

export default class NotaryService {
  client: AxiosInstance

  constructor(authService: AuthService, private store: RootStore) {
    this.client = axios.create()
    this.client.interceptors.request.use(async config => {
      console.log('intercept')
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

    this.store.commit('setFiles', files)
  }

  async uploadFile(file: File, hash: string) {
    const formData = new FormData()
    formData.append('file', file, file.name)
    const response = await this.client.post<FileInfo>(filesUrl, formData)
    const newFile = {
      ...response.data,
      hash,
    }

    this.store.commit('addFile', newFile)
  }
}
