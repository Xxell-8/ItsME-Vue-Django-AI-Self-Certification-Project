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
  checkMail (email) {
    return _axios({
      url: `accounts/email/`,
      method: 'post',
      data: { 'email': email }
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
  getUnapprovedUsers (code) {
    return _axios({
      url: `/accounts/pending/${code}/`,
      method: 'post'
    })
  },
  approveUser (userId) {
    return _axios({
      url: `/accounts/profile/approval/${userId}/`,
      method: 'put'
    })
  },
  getParnerInfo (code) {
    return _axios({
      url: `accounts/getpartner/${code}/`,
      method: 'post'
    })
  }

}