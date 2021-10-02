// import router from '@/router'

const state = {
  presentFaceImg: null,
  cardFaceImg: null,
  idCardImg: null,
}

const actions = {
  savePresentFace({ commit }, presentFaceImg) {
    commit('SAVE_PRESENT_FACE', presentFaceImg)
  },
  saveCardFace({ commit }, cardFaceImg) {
    commit('SAVE_CARD_FACE', cardFaceImg)
  },
  saveIdCard({ commit }, idCardImg) {
    commit('SAVE_ID_CARD', idCardImg)
  },
}

const mutations = {
  SAVE_PRESENT_FACE(state, presentFaceImg) {
    state.presentFaceImg = presentFaceImg
  },
  SAVE_CARD_FACE(state, cardFaceImg) {
    state.cardFaceImg = cardFaceImg
  },
  SAVE_ID_CARD(state, idCardImg) {
    state.idCardImg = idCardImg
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