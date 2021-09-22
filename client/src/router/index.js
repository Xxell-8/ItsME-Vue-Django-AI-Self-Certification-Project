import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/intro/Home.vue'
import Login from '@/views/partner/accounts/Login'

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
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
