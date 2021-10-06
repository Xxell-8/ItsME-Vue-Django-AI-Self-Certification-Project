<template>
  <div class="form">
    <div class="f-column">
      <span class="title font-mont fw-900 t-white">It's Me!</span>
      <span v-if="wrongInput" class="login-400 wrong">잘못된 이메일 혹은 비밀번호입니다.</span>
      <div class="account-inputs">
        <!-- 이메일 input -->
        <div class="account-input-box">
          <input
            id="email"
            class="account-input"
            v-model="email"
            type="text"
            @keyup.enter="onLogin(userData)"
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
            @keyup.enter="onLogin(userData)"
            required
          />
            <label>비밀번호</label>
          <div class="error-text" v-if="error.password">{{error.password}}</div>
        </div>
        <!-- 로그인 버튼 -->
        
        <button
          :class="[
            isSubmit ? 'btn-secondary' : 'btn-disabled', 
            'btn-submit font-mont fw-500'
          ]"
          @click="onLogin(userData)"
        >Login</button>
      </div>
      <!-- 페이지 이동 버튼 -->
      <div class="move-btns fw-200">
        <span class="t-white">아직 회원이 아니신가요?</span>
        <span
          class="btn t-white"
          @click="$router.push({ name: 'Accounts', params: { page: 'signup'}})"
        >회원가입</span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import PV from "password-validator"
import * as EmailValidator from "email-validator"

export default {
  name: 'Login',
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
    }
  },
  methods: {
    ...mapActions('accounts', ['onLogin']),
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
    },
    wrongInput: function() {
      if (this.wrongInput) {
        this.password = ''
      }
    }
  },
  computed: {
    ...mapState('accounts', ['wrongInput']),
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