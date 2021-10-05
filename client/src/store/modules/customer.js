// import router from '@/router'
import customerApi from '@/api/customer'

const state = {
  presentFaceImg: null,
  cardFaceImg: null,
  idCardImg: null,
  customerId: null,
  customerName: null,
  customerBirth: null,
  makedCard: null,
  faceSimilarity: null,
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
  async getVerificationResult({ commit, state }, path) {
    const payload = {
      id_card_image: state.idCardImg,
      face: state.presentFaceImg,
      id_card_face: state.cardFaceImg,
    }
    await customerApi.getVerificationResult(path, payload)
    .then((res) => {
      commit('GET_VERIFICATION_RESULT', res)
    })
    .catch((err) => {
      console.log(err)
    })
  }
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
  },
  GET_VERIFICATION_RESULT(state, res) {
    state.customerId = res.id
    state.customerName = res.names
    state.customerBirth = res.birth
    state.makedCard = res.id_card_image
    state.faceSimilarity = res.face_similarity
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