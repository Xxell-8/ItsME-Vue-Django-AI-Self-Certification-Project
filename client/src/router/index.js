import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/intro/Home.vue'
import Introduction from '@/views/customer/info/Introduction'
import FaceRecognition from '@/views/customer/verification/FaceRecognition'
import CardRecognition from '@/views/customer/verification/CardRecognition'
import Accounts from '@/views/partner/Accounts'
import PageNotFound from '@/views/error/PageNotFound'
import ServerError from '@/views/error/ServerError'

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
  {
    path: '/customer/introduction/',
    name: 'Index',
    component: Introduction
  },
  {
    path: '/customer/face-recognition/',
    name: 'FaceRecognition',
    component: FaceRecognition
  },
  {
    path: '/customer/card-recognition/',
    name: 'CardRecognition',
    component: CardRecognition
  },
  // Error
  { 
    path: '/:pathMatch(.*)*', 
    redirect: '/404'
  },
  {
    path: '/404',
    name: 'PageNotFound',
    component: PageNotFound
  },
  {
    path: '/500',
    name: 'ServerError',
    component: ServerError
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
