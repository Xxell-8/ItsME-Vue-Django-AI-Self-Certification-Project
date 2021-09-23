import axios from 'axios'
import router from '@/router'
import store from '@/store/index.js'

const _axios = axios.create({
  baseURL: process.env.VUE_APP_SERVER_URL,
  timeout: 10000,
})

_axios.interceptors.request.use(
  function (config) {
    config.headers['Authorization'] = `JWT ${store.state.accounts.acToken}`
    return config;
  }, 
  function (error) {
    return Promise.reject(error)
  }
)

_axios.interceptors.response.use(
  function (response) {
    // 토큰 자동 저장
    if (response.data.token) {
      store.commit('accounts/SET_ACCESS_TOKEN', response.data.token)
    }
    // if (response.data.refreshtoken) {
    //   store.commit('user/SET_REFRESH_TOKEN', response.data.refreshtoken)
    // }
    return Promise.resolve(response)
  },

  async function (error) {
    // JWT 관련 부분 백엔드에서 확정되면 다시 작성
    // 1. 토큰 만료 시, 토큰 refresh + 기존 요청
    // if (error.response.status === 401 && error.response.data.msg === 'AccessToken has been expired') {
    //   const originalRequest = error.config
    //   originalRequest.headers.refreshtoken = store.state.accounts.rfToken
    //   return _axios(originalRequest)
    // } else if (error.response.status === 401 && error.response.data.msg === 'RefreshToken has been expired') {
    // // 2. 액세스, 리프레쉬 모두 만료 시 로그아웃
    //   store.dispatch('user/onLogout')
    // }
    
    // 500 error 처리
    if (error.response.status >= 500) {
      router.push({ name: 'ServerError'})
    }
    return Promise.reject(error)
  }
)

export default _axios;