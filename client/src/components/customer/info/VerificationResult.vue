<template>
  <div class="f-column">
    <img class="logo-back" src="@/assets/image/logo/white-lg.svg" alt="logo">
    <!-- title -->
    <p class="title-small font-mont fw-700 t-white">Please Check</p>
    <p class="title-big font-mont fw-900 t-white">It's me!</p>
    <!-- notification -->
    <div class="notification f-column">
      <img class="partner-logo" :src=partnerLogo alt="partner logo">
      <div class="content-box">
        <p class="t-white">{{ verificationResult }}</p>
        <input type="text" v-model="name">
        <input type="text" v-model="birth">
      </div>
    </div>
    <!-- progress button -->
    <button @click="restart" class="btn-secondary btn-intro fw-700"><strong>본인 인증 다시 하기</strong></button>
    <button @click="finish" class="btn-secondary btn-intro fw-700"><strong>인증 정보 확인 및 제출</strong></button>
  </div>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'

export default {
  name: 'VerificationResult',
  props: {},
  data() {
    return {
      partnerLogo: 'https://edu.ssafy.com/asset/images/logo.png',
      name: null,
      birth: null,
    }  
  },
  async mounted() {
    await this.getVerificationResult(this.$store.state.customer.path)
    this.name = this.verificationResult.customerName;
    this.birth = this.verificationResult.customerBirth;
  },
  methods: {
    ...mapActions('customer', ['getVerificationResult', 'patchCustomerInfo']),
    ...mapMutations('customer', ['SAVE_PATH', 'RESET_STATE']),
    restart() {
      const path = this.$store.state.customer.path
      this.RESET_STATE()
      this.SAVE_PATH(path)
      this.$router.push('/customer/face-recognition/')
    },
    finish() {
      // 개인정보 인증 내역 patch
      const payload = {
        name: this.name,
        birth: this.birth,
        id_card: this.verificationResult.customerId
      }
      this.patchCustomerInfo(payload)
      // state 지워주기, 이름만 다음으로 보내기
      const name = this.name
      this.RESET_STATE()
      this.$emit('finish', name)
    }
  },
  computed: {
    verificationResult() {
      return {
        customerId: this.$store.state.customer.customerId,
        customerName: this.$store.state.customer.customerName,
        customerBirth: this.$store.state.customer.customerBirth,
        faceSimilarity: this.$store.state.customer.faceSimilarity,
      }
    }
  }
}
</script>