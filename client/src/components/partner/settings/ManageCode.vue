<template>
  <div class="code-box">
    <div class="f-row-between">
      <span>회사 CODE</span>
      <button
        class="btn btn-logout btn-outline fw-500"
        @click="onLogout"
      >로그아웃</button>
    </div>
    <div class="code">
      <span id="code">{{ hiddenCode }}</span>
      <img 
        src="@/assets/image/iconSvg/copy.svg" 
        alt=""
        @click="copyCode"
      >
    </div>
    <div class="copy-alert" style="display: none;">
      코드 복사 완료
    </div>
    <div>

    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'ManageCode',
  computed: {
    ...mapState('accounts', ['userInfo']),
    hiddenCode () {
      const code = this.userInfo.code
      return code.slice(0, 2) + '*'.repeat(code.length - 2)
    }
  },
  methods: {
    copyCode () {
      navigator.clipboard.writeText(this.userInfo.code)
        .then(() => {
          const alert = document.querySelector('.copy-alert')
          alert.style.display = 'block'
          setTimeout(() => {
            alert.style.display = 'none'
          }, 2000)
        })
    }
  }
}
</script>

<style>

</style>