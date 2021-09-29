import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store/'
import Home from '@/views/intro/Home.vue'
import Introduction from '@/views/customer/info/Introduction'
import FaceRecognition from '@/views/customer/verification/FaceRecognition'
import MotionRecognition from '@/views/customer/verification/MotionRecognition'
import CardRecognition from '@/views/customer/verification/CardRecognition'
import PartnerHome from '@/views/partner/Home'
import Accounts from '@/views/partner/Accounts'
import NewLink from '@/views/partner/NewLink'
import LinkList from '@/views/partner/LinkList'
import LinkDetail from '@/views/partner/LinkDetail'
import Settings from '@/views/partner/Settings'
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
    component: PartnerHome,
    meta: { requireAuth: true }
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
    path: '/partners/link/:id',
    name: 'LinkDetail',
    component: LinkDetail
  },
  {
    path: '/partners/accounts/:page',
    name: 'Accounts',
    component: Accounts
  },
  {
    path: '/partners/settings',
    name: 'Settings',
    component: Settings
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
    path: '/customer/motion-recognition',
    name: 'MotionRecognition',
    component: MotionRecognition
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

router.beforeEach(function (to, from, next) {
  if (to.matched.some(function(routeInfo) {
    return routeInfo.meta.requireAuth
  })) {
    if (!store.state.accounts.isLogin) {
      next('/partners/accounts/login')
    } else {
      next()
    }
  } else {
    if (to.name === 'Accounts') {
      if (store.state.accounts.isLogin) {
        next('/partners')
      } else {
        next()
      }
    } else {
      next()
    }
  }
  
})

export default router
