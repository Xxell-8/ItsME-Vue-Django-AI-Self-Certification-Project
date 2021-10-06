<template>
  <div class="partners">
    <div class="circle-primary"></div>
    <PartnerNav/>
    <UserNav/>
    <div class="body-with-nav">
      <div class="chapter f-column-start t-white">
        <div class="subtitle">회사 정보 관리</div>
        <div class="title">파트너 설정</div>
      </div>
      <div class="top-content">
        <ManageCode/>
        <CompanyInfo/>
      </div>
      <UserApproval/>
    </div>
  </div>
</template>

<script>
import './settings.scss'
import PartnerNav from '@/components/partner/common/PartnerNav'
import UserNav from '@/components/partner/common/UserNav'
import ManageCode from '@/components/partner/settings/ManageCode'
import CompanyInfo from '@/components/partner/settings/CompanyInfo'
import UserApproval from '@/components/partner/settings/UserApproval'

export default {
  name: 'Settings',
  components: {
    PartnerNav,
    UserNav,
    ManageCode,
    CompanyInfo,
    UserApproval
  },
}
</script>

<style>

</style>