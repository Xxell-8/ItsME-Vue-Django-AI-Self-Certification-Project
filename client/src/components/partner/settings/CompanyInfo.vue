<template>
  <div class="info-box shadow">
    <span class="setting-name">회사 정보</span>
    <div class="f-row info">
      <div class="f-column">
        <span class="cnt">{{ partnerInfo.userCnt }}</span>
        <span class="title">파트너 유저 수</span>
      </div>
      <div class="f-column">
        <span class="cnt">{{ partnerInfo.linkCnt }}</span>
        <span class="title">사용 중인 링크</span>
      </div>
      <div class="f-column">
        <span class="cnt">{{ unapprovedCnt }}</span>
        <span class="title">미승인 유저</span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex'

export default {
  name: 'CompanyInfo',
  computed: {
    ...mapGetters('accounts', ['unapprovedCnt']),
    ...mapState('partner', ['partnerInfo']),
    ...mapState('accounts', ['userInfo']),
  },
  methods: {
    ...mapActions('partner', ['getPartnerUserCnt', 'getPartnerLinkCnt'])
  },
  created () {
    this.getPartnerUserCnt(this.userInfo.code)
    this.getPartnerLinkCnt(this.userInfo.partnerId)
  }
}
</script>

<style>

</style>