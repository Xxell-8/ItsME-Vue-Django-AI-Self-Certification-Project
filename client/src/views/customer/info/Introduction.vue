<template>
  <div class="introduction">
    <img class="logo-back" src="@/assets/image/logo/white-lg.svg" alt="logo">
    <VerificationRequest/>
  </div>
</template>

<script>
import './info.scss'
import VerificationRequest from '@/components/customer/info/VerificationRequest.vue'

export default {
  name: 'Introduction',
  components: {
    VerificationRequest
  },
  props: {},
  data() {
    return {}  
  }
}
</script>