import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/intro/Home.vue'
import Accounts from '@/views/partner/Accounts'

const routes = [
  // B2B Home
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  // Partner
  {
    path: '/partners/accounts/:page',
    name: 'Accounts',
    component: Accounts
  },
  // Customer
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
