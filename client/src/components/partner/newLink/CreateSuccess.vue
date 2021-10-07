<template>
  <div class="link-alert">
    <div class="alert-box f-column-top">
      <i 
        class="fi fi-sr-cross-small exit-btn"
        @click="offSuccessModal(0)"
      ></i>
      <div class="header f-row">
        <img src="@/assets/image/logo/dark-sm.svg" alt="">
        <span class="font-mont">OK</span>
      </div>
      <div class="font-mont subtitle">A new link has been Created!</div>
      <div class="f-column new-link">
        <span class="name">{{ currentLink.name }}</span>
        <div class="path">
          <span>{{ path }}</span>
          <i 
            class="fi fi-rr-copy"
            @click="copyPath"
          ></i>
        </div>
        <span class="copy-msg">링크가 복사되었습니다!</span>
      </div>
      <button
        class="btn btn-primary fw-900"
        @click="offSuccessModal(1)"
      >상세 정보 보기</button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'CreateSuccess',
  computed: {
    ...mapState('partner', ['currentLink']),
    path () {
      return 'j5a204.p.ssafy.io/identify/' + this.currentLink.path
    }
  },
  methods: {
    ...mapActions('partner', ['offSuccessModal']),
    copyPath () {
      navigator.clipboard.writeText('https://'+ this.path)
        .then(() => {
          const alert = document.querySelector('.copy-msg')
          alert.style.opacity = 1
          setTimeout(() => {
            alert.style.opacity = 0
          }, 1500)
        })
    }
  }
}
</script>

<style>

</style>