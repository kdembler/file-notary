import Vue from 'vue'
import VueRouter, { NavigationGuard, RouteConfig } from 'vue-router'
import Upload from '@/views/Upload.vue'
import FilesList from '@/views/FilesList.vue'
import Register from '@/views/Register.vue'
import Login from '@/views/Login.vue'
import { UserService } from '@/services/user'

Vue.use(VueRouter)

const createRouter = (userService: UserService) => {
  const loggedInGuard: NavigationGuard = (_, __, next) => (userService.isLoggedIn ? next() : next('/login'))
  const notLoggedInGuard: NavigationGuard = (_, __, next) => (userService.isLoggedIn ? next('/') : next())

  const routes: RouteConfig[] = [
    {
      path: '/upload',
      component: Upload,
      beforeEnter: loggedInGuard,
    },
    {
      path: '/files',
      component: FilesList,
      beforeEnter: loggedInGuard,
    },
    {
      path: '/login',
      component: Login,
      beforeEnter: notLoggedInGuard,
    },
    {
      path: '/register',
      component: Register,
      beforeEnter: notLoggedInGuard,
    },
    {
      path: '*',
      redirect: '/upload',
    },
  ]

  return new VueRouter({ routes })
}

export default createRouter
