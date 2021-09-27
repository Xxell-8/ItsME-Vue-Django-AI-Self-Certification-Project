<template>
  <div class="left-nav f-column">
    <img 
      @click="$router.push({ name: 'PartnerHome'})"
      src="@/assets/image/logo/white-sm.svg" 
      alt="go to Home"
    >
    <i class="fi fi-sr-mode-portrait"></i>
    <i class="fi fi-sr-interactive"></i>
    <i class="fi fi-rr-alarm-clock"></i>
  </div>
</template>

<script>
export default {
  name: 'PartnerNav'
}
</script>

<style>

</style>