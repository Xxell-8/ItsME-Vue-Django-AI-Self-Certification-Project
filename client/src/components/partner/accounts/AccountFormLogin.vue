<template>
  <div class="f-column">
    <span class="title font-mont fw-900 t-white">It's Me!</span>
    <div class="account-inputs">
      <!-- 이메일 input -->
      <div class="account-input-box">
        <input
          id="email"
          class="account-input"
          v-model="email"
          type="text"
          @keyup.enter="login"
          autocapitalize="off"
          required
        />
          <label>이메일 계정</label>
        <div class="error-text" v-if="error.email">{{error.email}}</div>
      </div>
      <!-- 비밀번호 input -->
      <div class="account-input-box mt-2">
        <input
          id="password"
          class="account-input"
          v-model="password"
          type="password"
          @keyup.enter="login"
          required
        />
          <label>비밀번호</label>
        <div class="error-text" v-if="error.password">{{error.password}}</div>
      </div>
      <!-- 로그인 버튼 -->
      <button
        :class="[ isSubmit ? 'btn-secondary' : 'btn-disabled', 'btn-submit font-mont fw-500']"
        @click="login"
      >Login</button>
    </div>
    <div class="move-btns fw-200">
      <span
        class="btn t-white"
        @click="moveToSignup"
      >회원가입</span>
      <span class="t-white mx-1"> • </span>
      <span
        class="btn t-white"
        @click="moveToFindPassword"
      >비밀번호 찾기</span>
    </div>
  </div>
</template>

<script>
import PV from "password-validator"
import * as EmailValidator from "email-validator"

export default {
  name: 'AccountFormLogin',
  data: () => {
    return {
      email: '',
      password: '',
      passwordSchema: new PV(),
      error: {
        email: false,
        passowrd: false
      },
      isSubmit: false,
      wrongInput: false
    }
  },
  methods: {
    checkForm() {
      // 이메일 형식 검증
      if (this.email.length >= 0 && !EmailValidator.validate(this.email)) {
        this.error.email = "이메일 형식이 아닙니다."
      } else {
        this.error.email = false
      }
      // 비밀번호 형식 검증
      if (
        this.password.length >= 0 &&
        !this.passwordSchema.validate(this.password)
      ) {
        this.error.password = "영문, 숫자 포함 8자 이상이어야 합니다."
      } else {
        this.error.password = false
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
    email: function() {
      this.checkForm();
    },
    password: function() {
      this.checkForm();
    }
  },
  computed: {
    userData: function () {
      return {
        'email': this.email,
        'password': this.password
      }
    },
  },
  created() {
    this.passwordSchema
      .is()
      .min(8)
      .is()
      .max(100)
      .has()
      .digits()
      .has()
      .letters();
  }
}
</script>