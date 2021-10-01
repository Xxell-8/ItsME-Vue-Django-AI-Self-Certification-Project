import axios from 'axios'
import Cookies from "js-cookie"
import router from '@/router'
import accountsApi from './accounts.js'
import store from '@/store/index.js'

const _axios = axios.create({
  baseURL: process.env.VUE_APP_SERVER_URL,
  timeout: 10000,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  // withCredentials: true,
})

_axios.interceptors.request.use(
  function (config) {
    config.headers['Authorization'] = `Bearer ${store.state.accounts.acToken}`
    config.headers['X-CSRFToken'] = Cookies.get("csrftoken")
    return config;
  }, 
  function (error) {
    return Promise.reject(error)
  }
)

_axios.interceptors.response.use(
  function (response) {
    // 토큰 자동 저장
    if (response.data.access_token) {
      store.commit('accounts/SET_ACCESS_TOKEN', response.data.access_token)
    }
    if (response.data.access) {
      store.commit('accounts/SET_ACCESS_TOKEN', response.data.access)
    }
    if (response.data.refresh_token) {
      store.commit('accounts/SET_REFRESH_TOKEN', response.data.refresh_token)
    }
    return Promise.resolve(response)
  },

  async function (error) {
    // 토큰 만료 시, 토큰 refresh + 기존 요청
    if (error.response.status === 401 
      && error.response.data.code === 'token_not_valid') {
      const originalRequest = error.config
      await accountsApi.refreshToken()
      return _axios(originalRequest)
    } 
    
    // 500 error 처리
    if (error.response.status >= 500) {
      router.push({ name: 'ServerError'})
    }
    return Promise.reject(error)
  }
)

export default _axios;