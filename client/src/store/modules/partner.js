// import router from '@/router'
import partnerApi from '@/api/partner'

const state = {
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
    name: '임시 이름',
    path: 'adhlkqwkrjl1234'
  },
  successModal: false,
  linkList: null,
  linkInfo: null,
}

const actions = {
  async onCreateLink({ commit, dispatch }, linkData) {
    if (!linkData.name.length) {
      linkData.name = linkData.path
    }
    await partnerApi.createLink(linkData)
      .then((res) => {
        console.log(res)
        commit('SET_CURRENT_LINK', linkData)
        dispatch('onSuccessModal')
      })
      .catch((err) => {
        console.log(err.response)
      })
  },
  onSuccessModal({ commit }) {
    commit('SET_SUCCESS_MODAL', true)
  },
  offSuccessModal({ commit }) {
    commit('SET_SUCCESS_MODAL', false)
    commit('RESET_CURRENT_LINK')
  },
  async getLinkList ({ commit }) {
    await partnerApi.getLinkList()
      .then((res) => {
        console.log(res)
        commit('SET_LINK_LIST', res.data)
      })
  },
  async getLinkDetail ({ commit }, linkId) {
    await partnerApi.getLinkDetail(linkId)
      .then((res) => {
        console.log(res)
        commit('SET_LINK_INFO', res.data)
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
  SET_LINK_LIST (state, payload) {
    state.linkList = payload
  },
  SET_LINK_INFO (state, payload) {
    state.linkInfo = payload
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