<template>
  <div class="form">
    <div class="f-column">
      <div class="title-box">
        <span class="subtitle font-mont fw-300 t-white">It's Me!</span>
        <span class="title font-mont fw-900 t-white">Signup</span>
      </div>
      <div class="account-inputs">
        <!-- 이메일 input -->
        <div class="account-input-box">
          <input
            id="email"
            class="account-input"
            v-model="email"
            type="text"
            autocapitalize="off"
            required
          />
            <label>이메일 계정</label>
          <div class="error-text" v-if="error.email">{{error.email}}</div>
        </div>
        <!-- 비밀번호 input -->
        <div class="account-input-box">
          <input
            id="password"
            class="account-input"
            v-model="password"
            type="password"
            required
          />
            <label>비밀번호</label>
          <div class="error-text" v-if="error.password">{{error.password}}</div>
        </div>
        <!-- 비밀번호 확인 input -->
        <div class="account-input-box">
          <input
            id="passwordConfirm"
            class="account-input"
            v-model="passwordConfirm"
            type="password"
            required
          />
            <label>비밀번호 확인</label>
          <div class="error-text" v-if="error.passwordConfirm">{{error.passwordConfirm}}</div>
        </div>
        <!-- 이름 input -->
        <div class="account-input-box">
          <input
            id="name"
            class="account-input"
            v-model="name"
            type="text"
            autocapitalize="off"
            required
          />
            <label>이름</label>
          <div class="error-text" v-if="error.name">{{error.name}}</div>
        </div>
        <!-- 연락처 input -->
        <div class="account-input-box">
          <input
            id="phoneNum"
            class="account-input"
            v-model="phoneNum"
            type="text"
            maxlength="13"
            required
          />
            <label>휴대폰 번호</label>
          <div class="error-text" v-if="error.phoneNum">{{error.phoneNum}}</div>
        </div>
        <!-- 회원가입 버튼 -->
        <button
          :class="[ isSubmit ? 'btn-secondary' : 'btn-disabled', 'btn-submit font-mont fw-500']"
          @click="onSignup"
        >Signup</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import accountApi from '@/api/accounts.js'
import PV from "password-validator"
import * as EmailValidator from "email-validator"

export default {
  name: 'SignupForm',
  data: () => {
    return {
      email: '',
      password: '',
      passwordConfirm: '',
      name: '',
      phoneNum: '',
      passwordSchema: new PV(),
      error: {
        email: false,
        passowrd: false,
        passwordConfirm: false,
        name: false,
        phoneNum: false
      },
      isSubmit: false,
      wrongInput: false
    }
  },
  methods: {
    async onSignup () {
      await accountApi.signup(this.userInfo)
        .then((res) => {
          console.log(res)
          this.$store.commit('accounts/SET_TEMP_NAME', this.name)
          this.$emit('next')
        })
        .catch((err) => {
          console.log(err.response)
        })
    },
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
      // 비밀번호 확인 검증
      if (
        this.passwordConfirm.length >= 0 &&
        this.passwordConfirm != this.password
      ) {
        this.error.passwordConfirm = "비밀번호가 일치하지 않습니다."
      } else {
        this.error.passwordConfirm = false
      }
      // 이름 입력 안내
      if (!this.name.trim().length) {
        this.error.name = "이름을 입력해주세요."
      } else {
        this.error.name = false
      }
      if (this.phoneNum.length != 13) {
        this.error.phoneNum = "휴대폰번호 13자리를 입력해주세요."
      } else {
        this.error.phoneNum = false
      }
      // submit 가능 여부 확인
      let isSubmit = true;
      Object.values(this.error).map(v => {
        if (v) isSubmit = false;
      })
      this.isSubmit = isSubmit;
    },
    autoHypenPhone (str) {
      str = str.replace(/[^0-9]/g, '');
      var tmp = '';
      if (str.length < 4) {
        return str;
      } else if (str.length < 7) {
        tmp += str.substr(0, 3);
        tmp += '-';
        tmp += str.substr(3);
        return tmp;
      } else if(str.length < 11){
        tmp += str.substr(0, 3);
        tmp += '-';
        tmp += str.substr(3, 3);
        tmp += '-';
        tmp += str.substr(6);
        return tmp;
      } else{              
        tmp += str.substr(0, 3);
        tmp += '-';
        tmp += str.substr(3, 4);
        tmp += '-';
        tmp += str.substr(7);
        return tmp;
      }
    }
  },
  watch: {
    email: function() {
      this.checkForm();
    },
    password: function() {
      this.checkForm();
    },
    passwordConfirm: function() {
      this.checkForm();
    },
    name: function() {
      this.checkForm();
    },
    phoneNum: function() {
      this.phoneNum = this.autoHypenPhone(this.phoneNum)
      this.checkForm()
    }
  },
  computed: {
    ...mapState('accounts', ['companyInfo']),
    userInfo: function () {
      return {
        'email': this.email,
        'password1': this.password,
        'password2': this.passwordConfirm,
        'fullname': this.name,
        'name': this.companyInfo.name,
        'code': this.companyInfo.code,
        'phone': this.phoneNum,
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