// import router from '@/router'

const state = {
  acToken: '',
  rfToken: '',
}

const actions = {
  
}

const mutations = {
  SET_ACCESS_TOKEN(state, payload) {
    state.acToken = payload
  },
  SET_REFRESH_TOKEN(state, payload) {
    state.rfToken = payload
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