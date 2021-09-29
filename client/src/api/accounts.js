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
  getUserInfo (userId) {
    return _axios({
      url: `/accounts/profile/${userId}`,
      method: 'get'
    })
  },
  getPartnerList () {
    return _axios({
      url: '/accounts/partner',
      method: 'get'
    })
  },
  getUserList (companyCode) {
    return _axios({
      url: '/accounts/partner/getuser/',
      method: 'post',
      data: {'code': companyCode}
    })
  },

}