<template>
  <div class="partners">
    <div class="circle-primary"></div>
    <PartnerNav/>
    <UserNav/>
    <div class="body-with-nav">
      <div class="chapter f-column-start t-white">
        <div class="subtitle">본인 인증 데이터 관리</div>
        <div class="link-title">
          <div class="title">{{ linkInfo.name }}</div>
          <button
            :class="[fill ? 'complete': '', 'btn btn-outline fw-500']"
            @click="copyPath"
          >{{ copyMsg }}</button>
        </div>
      </div>
      <div v-if="linkInfo" class="expire-info">
        <span>{{ restTime }}<span>({{ expiredAt }})</span></span>에 링크가 자동 파기됩니다.
      </div>
      <LinkDetailTable/>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import { mapActions, mapState } from 'vuex'
import './linkDetail.scss'
import PartnerNav from '@/components/partner/common/PartnerNav'
import UserNav from '@/components/partner/common/UserNav'
import LinkDetailTable from '@/components/partner/link/LinkDetailTable'

export default {
  name: 'LinkDetail',
  components: {
    PartnerNav,
    UserNav,
    LinkDetailTable
  },
  data () {
    return {
      copyMsg: '링크 복사',
      fill: false
    }
  },
  methods: {
    ...mapActions('partner', ['getLinkDetail']),
    copyPath () {
      navigator.clipboard.writeText('https://j5a204.p.ssafy.io/identify/'+ this.linkInfo.path)
        .then(() => {
          this.copyMsg = '복사 완료'
          this.fill = true
          setTimeout(() => {
            this.copyMsg = '링크 복사'
            this.fill = false
          }, 1500)
        })
    }
  },
  computed: {
    ...mapState('partner', ['linkInfo']),
    expiredAt () {
      return moment(this.linkInfo.expired_at).locale('ko').format('lll')
    },
    restTime () {
      return moment(this.linkInfo.expired_at).locale('ko').endOf('hour').fromNow()
    },
  },
  created () {
    this.getLinkDetail(this.$route.params.id)
  }
}
</script>