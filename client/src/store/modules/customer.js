// import router from '@/router'
import customerApi from '@/api/customer'

const state = {
  path: null,
  presentFaceImg: null,
  cardFaceImg: null,
  idCardImg: null,
  customerId: null,
  customerName: null,
  customerBirth: null,
  maskedCard: null,
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
      commit('GET_VERIFICATION_RESULT', res.data)
    })
    .catch((err) => {
      console.log(err)
    })
  },
  patchCustomerInfo({ state }, payload) {
    customerApi.patchCustomerInfo(state.path, payload)
  }
}

const mutations = {
  SAVE_PATH(state, path) {
    state.path = path
  },
  SAVE_PRESENT_FACE(state, presentFaceImg) {
    state.presentFaceImg = presentFaceImg
  },
  SAVE_CARD_FACE(state, cardFaceImg) {
    state.cardFaceImg = cardFaceImg
  },
  SAVE_ID_CARD(state, idCardImg) {
    state.idCardImg = idCardImg
  },
  GET_VERIFICATION_RESULT(state, data) {
    state.customerId = data.id
    state.customerName = data.name
    state.customerBirth = data.birth
    state.maskedCard = data.id_card_image
    state.faceSimilarity = data.face_similarity
  },
  RESET_STATE(state) {
    state.path = null;
    state.presentFaceImg = null;
    state.cardFaceImg = null;
    state.idCardImg = null;
    state.customerId = null;
    state.customerName = null;
    state.customerBirth = null;
    state.maskedCard = null;
    state.faceSimilarity = null;
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