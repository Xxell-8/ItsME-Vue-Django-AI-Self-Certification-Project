<template>
  <div class="f-column">
    <!-- title -->
    <p class="title-small font-mont fw-700 t-white">Please Check</p>
    <p class="title-big font-mont fw-900 t-white">It's me!</p>
    <!-- notification -->
    <div class="notification f-column">
      <img class="partner-logo" :src=partnerLogo alt="partner logo">
      <div class="content-box">
        <span class="content fw-700 t-white">{{ task }}을 위해</span>
        <span class="content fw-700 t-white"><strong>{{ partner }}</strong>에서</span>
        <span class="content fw-700 t-white">본인인증을 요청합니다.</span>
        <br>
        <span class="content-small fw-700 t-white">본인 인증을 완료 시,</span>
        <span class="content-small fw-700 t-white"><span class="t-green">{{ afterProcess }}</span>를 확인하실 수 있습니다.</span>
      </div>
    </div>
    <!-- progress button -->
    <button @click="nextStep" class="btn-secondary btn-intro fw-700"><strong>고객 정보 제출하기</strong></button>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'VerificationResult',
  props: {},
  data() {
    return {
      partnerLogo: 'https://edu.ssafy.com/asset/images/logo.png',
      task: 'SW 역량테스트 진행',
      partner: 'SSAFY 사무국',
      afterProcess: 'TEST 입장 코드'
    }  
  },
  mounted() {
    this.getVerificationResult(this.$route.params.path)
  },
  methods: {
    ...mapActions('customer', ['getVerificationResult']),
    nextStep() {
      this.$router.push(`/customer/face-recognition/${this.$route.params.path}`)
    }
  },
  computed: {
    verificationResult() {
      return {
        customerId: this.$store.state.customer.customerId,
      }
    }
  }
}
</script>