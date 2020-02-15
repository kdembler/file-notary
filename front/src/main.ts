import Vue from 'vue'
import App from './App.vue'
import store from './store'
import vuetify from './plugins/vuetify'
import { AuthService } from '@/services/auth'
import createRouter from './router'
import NotaryService from '@/services/notary'

Vue.config.productionTip = false

const authService = new AuthService()
const notaryService = new NotaryService(authService, store)
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
