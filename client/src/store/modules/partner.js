import router from '@/router'
import partnerApi from '@/api/partner'

const state = {
  partnerInfo: {
    userCnt: null,
    linkCnt: null,
  },
  homeMenu: [
    {
      title: '신규 링크 생성',
      subtitle: '본인 인증 서비스',
      content: '고객에게 전송할<br/>본인 인증 서비스 링크를<br/>생성할 수 있습니다.',
      link: 'NewLink'
    },
    {
      title: '고객 정보 관리',
      subtitle: '본인 인증 데이터',
      content: '본인 인증 서비스를 통해<br/>전송 받은 고객 정보를<br/>관리할 수 있습니다.',
      link: 'LinkList'
    },
    {
      title: "템플릿 관리", 
      subtitle: "본인 인증 화면 관리", 
      content: "고객에게 전송할<br/>본인 인증 서비스 화면을<br/>커스터마이징할 수 있습니다.",
      link: null
    }
  ],
  currentLink: {
    name: null,
    path: null
  },
  successModal: false,
  deleteModal: false,
  linkList: null,
  linkInfo: null,
  
}

const actions = {
  // newLink
  async onCreateLink({ commit, dispatch }, linkData) {
    if (!linkData.name.length) {
      linkData.name = linkData.path
    }
    await partnerApi.createLink(linkData)
      .then(() => {
        // console.log(res)
        commit('SET_CURRENT_LINK', linkData)
        dispatch('onSuccessModal')
      })
      .catch((err) => {
        // console.log(err.response)
        if (err.response.data && Object.keys(err.response.data).includes('customers')) {
          alert('고객 데이터 형식이 맞는지 확인해주세요.')
        }
      })
  },
  onSuccessModal({ commit }) {
    commit('SET_SUCCESS_MODAL', true)
  },
  offSuccessModal({ state, commit }, to) {
    commit('SET_SUCCESS_MODAL', false)
    if (!to) {
      router.push({ name: 'PartnerHome'})
    } else {
      router.push({ name: 'LinkDetail', params: { id: state.currentLink.path }})
    }
    commit('RESET_CURRENT_LINK')
  },
  // 링크 삭제
  onDeleteModal({ commit }, linkData) {
    commit('SET_CURRENT_LINK', linkData)
    commit('SET_DELETE_MODAL', true)
  },
  offDeleteModal({ commit }) {
    commit('RESET_CURRENT_LINK')
    commit('SET_DELETE_MODAL', false)
  },
  async onDeleteLink ({ dispatch, commit }, linkId) {
    await partnerApi.deleteLink(linkId)
      .then(() => {
        // console.log(res)
        dispatch('getLinkList')
        commit('SET_DELETE_MODAL', false)
        commit('RESET_CURRENT_LINK')
      })
  },
  async getLinkList ({ commit }) {
    await partnerApi.getLinkList()
      .then((res) => {
        // console.log(res)
        commit('SET_LINK_LIST', res.data)
      })
  },
  async getLinkDetail ({ commit }, linkId) {
    await partnerApi.getLinkDetail(linkId)
      .then((res) => {
        // console.log(res)
        commit('SET_LINK_INFO', res.data)
      })
  },
  async getLinkDetailByComplete ({ commit }, linkId) {
    await partnerApi.getLinkDetailByComplete(linkId, 'completed_at')
      .then((res) => {
        // console.log(res)
        commit('SET_LINK_INFO', res.data)
      })
  },
  async getPartnerUserCnt ({ commit }, code) {
    await partnerApi.getPartnerCnt(code)
      .then((res) => {
        // console.log(res.data)
        commit('SET_USER_CNT', res.data.count)
      })
  },
  async getPartnerLinkCnt ({ commit }, partnerId) {
    await partnerApi.getPartnerLinkCnt(partnerId)
      .then((res) => {
        // console.log(res.data)
        commit('SET_LINK_CNT', res.data.link_count)
      })
  },

}

const mutations = {
  SET_CURRENT_LINK (state, payload) {
    state.currentLink.name = payload.name
    state.currentLink.path = payload.path
  },
  RESET_CURRENT_LINK (state) {
    state.currentLink.name = null
    state.currentLink.path = null
  },
  SET_SUCCESS_MODAL (state, payload) {
    state.successModal = payload
  },
  SET_DELETE_MODAL(state, payload) {
    state.deleteModal = payload
  },
  SET_LINK_LIST (state, payload) {
    state.linkList = payload
  },
  SET_LINK_INFO (state, payload) {
    state.linkInfo = payload
  },
  SET_USER_CNT (state, payload) {
    state.partnerInfo.userCnt = payload
  },
  SET_LINK_CNT (state, payload) {
    state.partnerInfo.linkCnt = payload
  },
  
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