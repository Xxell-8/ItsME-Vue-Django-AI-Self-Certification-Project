import _axios from "./interceptor"

export default {
  createLink (linkData) {
    return _axios({
      url: '/info/link/',
      method: 'post',
      data: linkData
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
      url: `/info/link/${linkId}`,
      method: 'get'
    })
  },

}