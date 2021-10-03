import _axios from "./interceptor"

export default {
  getVerificationResult (payload) {
    return _axios({
      url: '',
      method: 'post',
      data: payload
    })
  }
}