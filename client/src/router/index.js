import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/intro/Home.vue'
import PartnerHome from '@/views/partner/Home'
import Accounts from '@/views/partner/Accounts'
import NewLink from '@/views/partner/NewLink'
import LinkList from '@/views/partner/LinkList'
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
    path: '/partners',
    name: 'PartnerHome',
    component: PartnerHome
  },
  {
    path: '/partners/link/new',
    name: 'NewLink',
    component: NewLink
  },
  {
    path: '/partners/link',
    name: 'LinkList',
    component: LinkList
  },
  {
    path: '/partners/accounts/:page',
    name: 'Accounts',
    component: Accounts
  },
  // Customer
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
