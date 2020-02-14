import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Upload from '@/views/Upload.vue'
import FilesList from '@/views/FilesList.vue'
import Register from '@/views/Register.vue'
import Login from '@/views/Login.vue'

Vue.use(VueRouter)

const routes: RouteConfig[] = [
  {
    path: '/upload',
    component: Upload,
  },
  {
    path: '/files',
    component: FilesList,
  },
  {
    path: '/login',
    component: Login,
  },
  {
    path: '/register',
    component: Register,
  },
  {
    path: '*',
    redirect: '/upload',
  },
]

const router = new VueRouter({ routes })

export default router
