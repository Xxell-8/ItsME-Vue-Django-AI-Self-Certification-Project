<template>
  <div class="form">
    <div class="f-column">
      <div class="title-box">
        <span class="deco font-mont fw-300 t-white">Welcome to</span>
        <span class="title font-mont fw-900 t-white">
          It's <span class="t-secondary">Me</span>!
        </span>
      </div>
      <div class="f-column t-center">
        <div class="main-text t-white">
          <span class="fw-900">{{ tempName }}</span>님,<br/>
          환영합니다.
        </div>
        <div class="sub-text t-white fw-200">
          <span class="fw-500">기업명</span> 담당자의 가입 승인 후,<br/>
          잇츠미 서비스 이용이 가능합니다.
        </div>
      </div>
      <button
        class="btn-secondary btn-submit font-mont fw-500"
        @click="$router.push({ name: 'Accounts', params: {page: 'login'}})"
      >OK</button>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'SignupComplete',
  computed: {
    ...mapState('accounts', ['tempName'])
  }
}
</script>