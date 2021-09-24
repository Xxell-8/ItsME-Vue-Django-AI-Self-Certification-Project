import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/intro/Home.vue'
import Login from '@/views/partner/accounts/Login'
import Introduction from '@/views/customer/info/Introduction'
import FaceRecognition from '@/views/customer/verification/FaceRecognition'

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
  },
  {
    path: '/customer/face-recognition/',
    name: 'FaceRecognition',
    component: FaceRecognition
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
