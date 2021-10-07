<template>
  <div class="f-column">
    <img class="logo-back" src="@/assets/image/logo/white-lg.svg" alt="logo">
    <!-- title -->
    <div class="title-container">
      <p class="title-small font-mont fw-700 t-white">Please Check</p>
      <p class="title-big font-mont fw-900 t-white">It's me!</p>
    </div>
    <!-- notification -->
    <div class="notification f-column">
      <!-- 얼굴 비교 결과 실패 시 -->
      <div v-if="isSimilar===false" class="content-fail f-column">
        <div class="title-container">
          <span class="fw-500 t-white content-title">본인 확인에 실패했습니다.</span>
          <span class="fw-500 t-white content-title">다시 시도해주세요.</span>
        </div>
        <div class="detail-box">
          <p class="fw-300 t-white">촬영된 얼굴과 신분증 사진의 </p>
          <p class="fw-300 t-white">유사도가 낮습니다.</p>
          <p class="fw-300 t-white">본인의 사진이더라도, 초점이 흐리거나</p>
          <p class="fw-300 t-white">빛이 반사되면 인증에 실패할 수 있습니다.</p>
        </div>
      </div>
      <!-- 얼굴 비교 결과 성공 시 -->
      <div v-if="isSimilar===true" class="content-success">
        <div class="title-container">
          <span class="fw-500 t-white content-title">본인 확인에 성공했습니다!</span>
        </div>
        <div class="detail-box">
          <p class="fw-300 t-white">신분증 정보를 확인하시고</p>
          <p class="fw-300 t-white">잘못 인식된 부분이 있다면 수정해주세요.</p>
          </div>
        <div class="account-inputs">
        <!-- 이메일 input -->
        <div class="account-input-box">
          <input
            class="account-input"
            v-model="name"
            type="text"
            required
          />
            <label>이름</label>
          <div class="error-text" v-if="error.name">{{error.name}}</div>
        </div>
        <!-- 비밀번호 input -->
        <div class="account-input-box mt-2">
          <input
            class="account-input"
            v-model="birth"
            type="text"
            @keyup.enter="onLogin(userData)"
            required
            maxlength="6"
          />
            <label>생년월일</label>
          <div class="error-text" v-if="error.birth">{{error.birth}}</div>
        </div>
      </div>
      </div>
    </div>
    <!-- progress button -->
    <div class="btn-container">
      <!-- 얼굴 비교 결과 실패 시 -->
      <button v-show="isSimilar===false" @click="restart" class="btn-secondary btn-intro fw-700"><strong>본인 인증 다시 하기</strong></button>
      <!-- 얼굴 비교 결과 성공 시 -->
      <button v-show="isSimilar===true" @click="finish" class="btn-secondary btn-intro fw-700"><strong>인증 정보 확인 및 제출</strong></button>
    </div>
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
      name: '',
      birth: '',
      isSimilar: null,
      error: {
        name: false,
        birth: false,
      }
    }  
  },
  async mounted() {
    await this.getVerificationResult(this.$store.state.customer.path)
    this.name = this.verificationResult.customerName;
    this.birth = this.verificationResult.customerBirth;
    this.isSimilar = this.verificationResult.faceSimilarity;
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
    },
    checkForm() {
      // 이름 형식 검증
      if (this.name.length < 2) {
        this.error.name = "올바른 이름을 입력해주세요."
      } else {
        this.error.name = false
      }
      // 생년월일 형식 검증
      if (this.birth.length < 6 || isNaN(this.birth)) {
        this.error.birth = "6자리 숫자를 입력해주세요(ex. 211006)"
      } else {
        this.error.birth = false
      }
      // submit 가능 여부 확인
      /* let isSubmit = true;
      Object.values(this.error).map(v => {
        if (v) isSubmit = false;
      })
      this.isSubmit = isSubmit; */
    },
  },
  watch: {
    name: function() {
      this.checkForm();
    },
    birth: function() {
      this.checkForm();
    },
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