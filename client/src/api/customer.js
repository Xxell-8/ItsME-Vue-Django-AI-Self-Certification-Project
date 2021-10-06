import _axios from "./interceptor"

export default {
  getVerificationResult (path, payload) {
    return _axios({
      url: `/info/link/${path}/id_card_ocr/`,
      method: 'post',
      data: payload
    })
  },
  patchCustomerInfo (path, payload) {
    return _axios({
      url: `/info/link/${path}/customer/`,
      method: 'patch',
      data: payload
    })
  }
}