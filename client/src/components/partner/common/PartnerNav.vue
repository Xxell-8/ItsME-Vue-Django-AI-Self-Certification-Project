<template>
  <div class="left-nav f-column-top">
    <img 
      @click="$router.push({ name: 'PartnerHome'})"
      src="@/assets/image/logo/white-sm.svg" 
      alt="go to Home"
    >
    <img
      class="icon" 
      src="@/assets/image/icon/user.svg"
      alt="고객 정보 관리"
      title="고객 정보 관리"
      @click="$router.push({ name: 'LinkList' })"
    >
    <img
      class="icon" 
      src="@/assets/image/icon/newlink.svg"
      alt="신규 링크 생성"
      title="신규 링크 생성"
      @click="$router.push({ name: 'NewLink' })"
    >
    <img
      class="icon" 
      src="@/assets/image/icon/company.svg"
      alt="회사 설정"
    >
  </div>
</template>

<script>
export default {
  name: 'PartnerNav'
}
</script>

<style>

</style>