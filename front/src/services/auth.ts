import axios from 'axios'
import jwt from 'jsonwebtoken'
import { loginUrl, registerUrl } from '@/urls'

const TOKEN_KEY = 'FILE_NOTARY-TOKEN'

type LoginResponse = { access_token: string }
type RegisterResponse = { access_token: string; user_code: string }

export class AuthService {
  get isLoggedIn() {
    return !!this.getToken()
  }

  get userCode(): string | null {
    const token = this.getToken()
    if (!token) {
      return null
    }
    const decoded = jwt.decode(token)
    if (!decoded) return null
    return decoded.sub
  }

  async logIn(userCode: string) {
    const payload = { user_code: userCode }
    const response = await axios.post<LoginResponse>(loginUrl, payload)
    const token = response.data.access_token
    this.setToken(token)
  }

  async register() {
    const response = await axios.post<RegisterResponse>(registerUrl)
    const { access_token: token, user_code: userCode } = response.data
    this.setToken(token)
    return userCode
  }

  logOut() {
    window.localStorage.removeItem(TOKEN_KEY)
  }

  getToken() {
    return window.localStorage.getItem(TOKEN_KEY)
  }

  private setToken(token: string) {
    window.localStorage.setItem(TOKEN_KEY, token)
  }
}
