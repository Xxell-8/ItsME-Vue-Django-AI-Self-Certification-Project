import _axios from "./interceptor"

export default {
  signup(userData) {
    return _axios({
      url: '/accounts/registration',
      method: 'post',
      data: userData
    })
  },
  login(userData) {
    return _axios({
      url: 'accounts/login/',
      method: 'post',
      data: userData
    })
  },

  getPartnerList () {
    return _axios({
      url: '/accounts/partner',
      method: 'get'
    })
  }
}