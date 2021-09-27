<template>
  <div class="partners">
    <div class="circle-primary"></div>
    <PartnerNav/>
    <UserNav/>
    <div class="body-with-nav">
      <div class="header f-column-start t-white">
        <div class="subtitle">안녕하세요,</div>
        <div class="title"><span>{{ company }} {{ user }}</span>님</div>
      </div>
      <HomeMenu/>
    </div>
  </div>
</template>

<script>
import './common.scss'
import './home.scss'
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
  data () {
    return {
      user: '우만승',
      company: 'SSAFY'
    }
  }
}
</script>

<style>

</style>