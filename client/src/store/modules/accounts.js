import router from '@/router'
import accountApi from '@/api/accounts'

const state = {
  acToken: null,
  rfToken: null,
  tempName: null,
  companyInfo: null,
  isLogin: false,
  userInfo: null,
}

const actions = {
  moveToPartnerHome () {
    router.push({ name: 'PartnerHome' })
  },
  async onLogin({ dispatch, commit }, userData) {
    // console.log(userData)
    await accountApi.login(userData)
      .then((res) => {
        // console.log(res)
        commit('SET_IS_LOGIN', true)
        dispatch('getUserInfo', res.data.user.pk)
        dispatch('moveToPartnerHome')
      })
  },
  async getUserInfo({ commit }, userId) {
    await accountApi.getUserInfo(userId)
      .then((res) => {
        commit('SET_USER_INFO', res.data)
      })
  },
  onLogout({ commit }) {
    commit('SET_IS_LOGIN', false)
    commit('SET_ACCESS_TOKEN', null)
    commit('SET_REFRESH_TOKEN', null)
    commit('SET_USER_INFO', null)
    router.push('/partners/accounts/login')
  }
  
}

const mutations = {
  SET_ACCESS_TOKEN(state, payload) {
    state.acToken = payload
  },
  SET_REFRESH_TOKEN(state, payload) {
    state.rfToken = payload
  },
  SET_TEMP_NAME(state, payload) {
    state.tempName = payload
  },
  SET_COMPANY_INFO(state, payload) {
    state.companyInfo = payload
  },
  SET_IS_LOGIN (state, payload) {
    state.isLogin = payload
  },
  SET_USER_INFO (state, payload) {
    state.userInfo = payload
  }
}

const getters = {

}

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
}