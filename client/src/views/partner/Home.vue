<template>
  <div class="partners">
    <div class="circle-primary"></div>
    <PartnerNav/>
    <UserNav/>
    <div class="body-with-nav">
      <div v-if="userInfo" class="header f-column-start t-white">
        <div class="subtitle">안녕하세요,</div>
        <div class="title"><span>{{ userInfo.name }} {{ userInfo.fullname }}</span>님</div>
        <div v-if="!userInfo.approval">관리자 승인 이후 서비스 이용이 가능합니다.</div>
      </div>
      <HomeMenu/>
    </div>
  </div>
</template>

<script>
import './common.scss'
import './home.scss'
import { mapState } from 'vuex'
import PartnerNav from '@/components/partner/common/PartnerNav'
import UserNav from '@/components/partner/common/UserNav'
import HomeMenu from '@/components/partner/home/HomeMenu'
export default {
  name: 'PartnersHome',
  components: {
    PartnerNav,
    UserNav,
    HomeMenu
  },
  computed: {
    ...mapState('accounts', ['userInfo'])
  }
}
</script>

<style>

</style>