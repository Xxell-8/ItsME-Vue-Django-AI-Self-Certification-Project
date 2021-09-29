// import router from '@/router'

const state = {
  homeMenu: [
    {
      title: '신규 링크 생성',
      subtitle: '본인 인증 서비스',
      content: '고객에게 전송할<br/>본인 인증 서비스 링크를<br/>생성할 수 있습니다.',
      link: 'NewLink'
    },
    {
      title: '고객 정보 관리',
      subtitle: '본인 인증 데이터',
      content: '본인 인증 서비스를 통해<br/>전송 받은 고객 정보를<br/>관리할 수 있습니다.',
      link: 'LinkList'
    },
    {
      title: "템플릿 관리", 
      subtitle: "본인 인증 화면 관리", 
      content: "고객에게 전송할<br/>본인 인증 서비스 화면을<br/>커스터마이징할 수 있습니다.",
      link: null
    }
  ]
}

const actions = {
  
}

const mutations = {

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