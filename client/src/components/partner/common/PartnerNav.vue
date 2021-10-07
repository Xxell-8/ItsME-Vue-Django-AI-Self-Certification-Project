<template>
  <div class="left-nav f-column-top">
    <img 
      class="logo-img"
      @click="$router.push({ name: 'PartnerHome'})"
      src="@/assets/image/logo/white-sm.svg" 
      alt="go to Home"
    >
    <i 
      class="icon fi fi-sr-mode-portrait"
      title="고객 정보 관리"
      @click="$router.push({ name: 'LinkList' })"
    ></i>
    <i 
      class="icon fi fi-sr-interactive"
      title="신규 링크 생성"
      @click="$router.push({ name: 'NewLink' })"
    ></i>
    <i 
      v-if="userInfo && userInfo.auth"
      class="fi fi-sr-building icon"
      @click="$router.push({ name: 'Settings' })"
    ></i>
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