<template>
  <div class="form">
    <div class="f-column">
      <div class="title-box">
        <span class="subtitle font-mont fw-300 t-white">It's Me!</span>
        <span class="title font-mont fw-900 t-white">Signup</span>
      </div>
      <div class="account-inputs">
        <!-- 소속 회사명 Select -->
        <div class="account-input-box">
          <input 
            id="company"
            list="list"
            class="account-input"
            v-model="company"
            type="text"
            @keyup.enter="login"
            autocapitalize="off"
            required
          />
          <datalist id ="list">
            <option
              v-for="(partner, idx) in partners"
              :key="idx"
            >{{partner}}</option>
          </datalist>
          <label>소속 회사명</label>
          <div class="error-text" v-if="error.company">{{error.company}}</div>
        </div>
        <!-- 회사 코드 input -->
        <div class="account-input-box">
          <input
            id="code"
            class="account-input"
            v-model="code"
            type="text"
            @keyup.enter="login"
            autocapitalize="off"
            required
          />
            <label>소속 회사 CODE</label>
          <div class="error-text" v-if="error.code">{{error.code}}</div>
        </div>
        <!-- 로그인 버튼 -->
        <button
          :class="[ isSubmit ? 'btn-secondary' : 'btn-disabled', 'btn-submit font-mont fw-500']"
          @click="login"
        >Next</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignupCert',
  data: () => {
    return {
      partners: [
        'sample1',
        'sample2',
        'sample3',
        'sample4',
        'sample5',
        'sample6',
      ],
      company: '',
      code: '',
      error: {
        company: false,
        code: false
      },
      isSubmit: false,
      wrongInput: false
    }
  },
  methods: {
    checkForm() {
      // 이메일 형식 검증
      if (!this.company.trim().length) {
        this.error.company = "소속 회사를 선택해주세요."
      } else if (this.company && !this.partners.includes(this.company)){
        this.error.company = "회사명을 올바르게 선택해주세요."
      } else {
        this.error.company = false
      }
      // 비밀번호 형식 검증
      if (!this.code.trim().length) {
        this.error.code = "회사 코드를 입력해주세요."
      } else {
        this.error.code = false
      }
      // submit 가능 여부 확인
      let isSubmit = true;
      Object.values(this.error).map(v => {
        if (v) isSubmit = false;
      })
      this.isSubmit = isSubmit;
    },
  },
  watch: {
    company: function() {
      this.checkForm();
    },
    code: function() {
      this.checkForm();
    }
  },
  computed: {
    userData: function () {
      return {
        'company': this.company,
        'code': this.code
      }
    },
  },
}
</script>

<style lang="scss" scoped>
  input::-webkit-calendar-picker-indicator {
    opacity: 0.8;
  }
</style>