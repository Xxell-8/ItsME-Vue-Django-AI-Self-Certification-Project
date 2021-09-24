import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/intro/Home.vue'
import Login from '@/views/partner/accounts/Login'
import Introduction from '@/views/customer/info/Introduction'

const routes = [
  // B2B Home
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  // Partner
  {
    path: '/partners/login',
    name: 'Login',
    component: Login
  },
  // Customer
  {
    path: '/customer/introduction/',
    name: 'Index',
    component: Introduction
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
