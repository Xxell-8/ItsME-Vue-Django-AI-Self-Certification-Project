import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/intro/Home.vue'

const routes = [
  // B2B Home
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  // Partner

  // Customer
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
