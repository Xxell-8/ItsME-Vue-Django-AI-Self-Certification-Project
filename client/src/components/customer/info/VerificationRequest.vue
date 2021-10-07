<template>
  <div class="f-column">
    <!-- title -->
    <p class="title-small font-mont fw-700 t-white">Welcome to</p>
    <p class="title-big font-mont fw-900 t-white">It's Me!</p>
    <!-- notification -->
    <div class="notification f-column">
      <div class="content-box">
        <span class="content fw-700 t-white">
          <span 
            class="t-primary fw-900"
            v-if="partner"  
          >{{ partner }}</span> 
          에서
        </span>
        <span class="content fw-700 t-white">본인인증을 요청했습니다.</span>
        <br>
        <span class="content-small fw-700 t-white">본인 인증을 위해</span>
        <span class="content-small fw-700 t-white"><span class="t-green">얼굴 인식과 모션 인식,<br/> 신분증 촬영</span>이 진행됩니다.</span>
      </div>
    </div>
    <!-- progress button -->
    <button @click="nextStep" class="btn-secondary btn-intro fw-700"><strong>본인 인증 하러 가기</strong></button>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
import customerApi from '@/api/customer.js'

export default {
  name: 'VerificationRequest',
  props: {},
  data() {
    return {
      partner: null,
    }  
  },
  methods: {
    ...mapMutations('customer', ['SAVE_PATH', 'RESET_STATE']),
    nextStep() {
      this.$router.push('/customer/face-recognition')
    }
  },
  async created () {
    this.RESET_STATE()
    const path = this.$route.params.path
    await customerApi.getLinkPartner(path)
      .then((res) => {
        this.partner = res.data.name
      })
    this.SAVE_PATH(path)
  }
}
</script>