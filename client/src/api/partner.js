import _axios from "./interceptor"

export default {
  createLink (linkData) {
    return _axios({
      url: '/info/link/',
      method: 'post',
      data: linkData
    })
  },
  deleteLink (linkId) {
    return _axios({
      url: `/info/link/${linkId}/`,
      method: 'delete'
    })
  },
  getLinkList () {
    return _axios({
      url: '/info/link/',
      method: 'get'
    })
  },
  getLinkDetail (linkId) {
    return _axios({
      url: `/info/link/${linkId}/`,
      method: 'get'
    })
  },
  getPartnerCnt (code) {
    return _axios({
      url: `/accounts/count/${code}/`,
      method: 'post'
    })
  },
  getPartnerLinkCnt (partnerId) {
    return _axios({
      url: `/info/link/partner/${partnerId}/`,
      method: 'get'
    })
  },
}