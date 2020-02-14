import Vue from 'vue'
import App from './App.vue'
import store from './store'
import vuetify from './plugins/vuetify'
import { UserService } from '@/services/user'
import createRouter from './router'

Vue.config.productionTip = false

const userService = new UserService()
const router = createRouter(userService)

new Vue({
  store,
  vuetify,
  router,
  provide: {
    userService,
  },
  render: h => h(App),
}).$mount('#app')
