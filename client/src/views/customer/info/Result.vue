<template>
  <div class="result">
    <img class="logo-back" src="@/assets/image/logo/white-lg.svg" alt="logo">
    <Loading v-if="faceSimilarity===null"/>
    <VerificationResult v-show="faceSimilarity!==null"/>
  </div>
</template>

<script>
import './info.scss'
import Loading from '@/components/customer/verification/Loading.vue'
import VerificationResult from '@/components/customer/info/VerificationResult.vue'

export default {
  name: 'Result',
  components: {
    Loading,
    VerificationResult
  },
  props: {},
  data() {
    return {
    }  
  },
  computed: {
    faceSimilarity() {
      return this.$store.state.customer.faceSimilarity
    }
  },
}
</script>