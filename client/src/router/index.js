import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store/'
import Home from '@/views/intro/Home.vue'
import Introduction from '@/views/customer/info/Introduction'
import Result from '@/views/customer/info/Result'
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
    component: NewLink,
    meta: { requireAuth: true }
  },
  {
    path: '/partners/link',
    name: 'LinkList',
    component: LinkList,
    meta: { requireAuth: true }
  },
  {
    path: '/partners/link/:id',
    name: 'LinkDetail',
    component: LinkDetail,
    meta: { requireAuth: true }
  },
  {
    path: '/partners/accounts/:page',
    name: 'Accounts',
    component: Accounts
  },
  {
    path: '/partners/settings',
    name: 'Settings',
    component: Settings,
    meta: { requireAuth: true }
  },
  // Customer
  {
    path: '/identify/:path',
    name: 'Index',
    component: Introduction
  },
  {
    path: '/customer/face-recognition/',
    name: 'FaceRecognition',
    component: FaceRecognition
  },
  {
    path: '/customer/motion-recognition/',
    name: 'MotionRecognition',
    component: MotionRecognition
  },
  {
    path: '/customer/card-recognition/',
    name: 'CardRecognition',
    component: CardRecognition
  },
  {
    path: '/customer/result/',
    name: 'Result',
    component: Result,
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
    if (to.name === 'Settings') {
      if (!store.state.accounts.isLogin || !store.state.accounts.userInfo.auth) {
        next('/partners')
      } else {
        next()
      }
    } else if (to.name === 'NewLink' || to.name === 'LinkList' || to.name === 'LinkDetail') {
      if (!store.state.accounts.isLogin || !store.state.accounts.userInfo.approval) {
        next('/partners')
      } else {
        next()
      }
    } else {
      if (!store.state.accounts.isLogin) {
        next('/partners/accounts/login')
      } else {
        next()
      }
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
