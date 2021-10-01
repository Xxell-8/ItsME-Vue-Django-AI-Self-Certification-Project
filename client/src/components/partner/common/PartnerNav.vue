<template>
  <div class="left-nav f-column-top">
    <img 
      class="logo-img"
      @click="$router.push({ name: 'PartnerHome'})"
      src="@/assets/image/logo/white-sm.svg" 
      alt="go to Home"
    >
    <img
      class="icon" 
      src="@/assets/image/iconSvg/user.svg"
      alt="고객 정보 관리"
      title="고객 정보 관리"
      @click="$router.push({ name: 'LinkList' })"
    >
    <img
      class="icon" 
      src="@/assets/image/iconSvg/newlink.svg"
      alt="신규 링크 생성"
      title="신규 링크 생성"
      @click="$router.push({ name: 'NewLink' })"
    >
    <img
      v-if="userInfo && userInfo.auth"
      class="icon" 
      src="@/assets/image/iconSvg/company.svg"
      alt="회사 설정"
      @click="$router.push({ name: 'Settings' })"
    >
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'PartnerNav',
  computed: {
    ...mapState('accounts', ['userInfo'])
  }
}
</script>

<style>

</style>