import router from '@/router'
import accountApi from '@/api/accounts'

const state = {
  acToken: null,
  rfToken: null,
  tempName: null,
  companyInfo: null,
  isLogin: false,
  userInfo: null,
  unapprovedUsers: [],
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
  async getUserInfo({ commit, dispatch }, userId) {
    await accountApi.getUserInfo(userId)
      .then((res) => {
        commit('SET_USER_INFO', res.data)
        dispatch('getPartnerInfo')
      })
  },
  async getPartnerInfo({ state, commit }) {
    await accountApi.getParnerInfo(state.userInfo.code)
      .then((res) => {
        // console.log(res.data)
        commit('ADD_PARTNER_INFO', res.data.id)
      })
      .catch((err) => {
        console.log(err.response)
      })
  },
  onLogout({ commit }) {
    commit('SET_IS_LOGIN', false)
    commit('SET_ACCESS_TOKEN', null)
    commit('SET_REFRESH_TOKEN', null)
    commit('SET_USER_INFO', null)
    router.push('/partners/accounts/login')
  }, 
  async getUnapprovedUsers ({ state, commit }) {
    await accountApi.getUnapprovedUsers(state.userInfo.code)
      .then((res) => {
        console.log(res)
        if (res.status === 200) {
          commit('SET_UNAPPROVED_USR', res.data)
        }
      })
  },
  async onApproveUser({ dispatch }, userId) {
    await accountApi.approveUser(userId)
      .then(() => {
        dispatch('getUnapprovedUsers')
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
  },
  SET_COMPANY_INFO(state, payload) {
    state.companyInfo = payload
  },
  SET_IS_LOGIN (state, payload) {
    state.isLogin = payload
  },
  SET_USER_INFO (state, payload) {
    state.userInfo = payload
  },
  ADD_PARTNER_INFO (state, payload) {
    state.userInfo.partnerId = payload
  },
  SET_UNAPPROVED_USR (state, payload) {
    state.unapprovedUsers = payload
  }
}

const getters = {
  unapprovedCnt: (state) => {
    return state.unapprovedUsers.length
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
}