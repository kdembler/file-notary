import Vue from 'vue'
import App from './App.vue'
import store from './store'
import vuetify from './plugins/vuetify'
import { AuthService } from '@/services/auth'
import createRouter from './router'
import NotaryService from '@/services/notary'
import Web3Service from '@/services/web3'

Vue.config.productionTip = false

const authService = new AuthService()
const web3Service = new Web3Service()
const notaryService = new NotaryService(authService, store, web3Service)

const router = createRouter(authService)

new Vue({
  store,
  vuetify,
  router,
  provide: {
    authService,
    notaryService,
  },
  render: h => h(App),
}).$mount('#app')
