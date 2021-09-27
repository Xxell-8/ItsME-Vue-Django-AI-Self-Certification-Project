// import router from '@/router'
import accountApi from '@/api/accounts'

const state = {
  acToken: '',
  rfToken: '',
  tempName: '',
}

const actions = {
  async onSignup({ commit }, userData) {
    console.log(userData)
    await accountApi.signup(userData)
      .then((res) => {
        console.log(res)
        commit('SET_TEMP_NAME', userData.name)
      })
  },
  async onLogin({ commit }, userData) {
    console.log(userData)
    await accountApi.login(userData)
      .then((res) => {
        console.log(res)
        commit('SET_TEMP_NAME', userData.email)
      })
  },
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