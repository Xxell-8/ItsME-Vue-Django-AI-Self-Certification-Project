<template>
  <div class="code-box shadow">
    <span class="setting-name">회사 CODE</span>
    <div class="code">
      <span v-if="hidden" class="space">{{ hiddenCode }}</span>
      <span v-else>{{ userInfo.code }}</span>
      <i 
        class="fi fi-rr-copy"
        @click="copyCode"
      ></i>
      <i 
        :class="[hidden ? 'fi-rr-eye' : 'fi-rr-eye-crossed', 'fi eye']"
         @click="changeHidden"
      ></i>
      <div class="copy-msg" style="display: none;">
        회사 CODE가 복사되었습니다!
      </div>
    </div>
    <div>

    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'ManageCode',
  data () {
    return {
      hidden: true,
    }
  },
  computed: {
    ...mapState('accounts', ['userInfo']),
    hiddenCode () {
      if (this.userInfo) {
        const code = this.userInfo.code
        return code.slice(0, 2) + '•'.repeat(code.length - 2)
      }
      return ''
    },
  },
  methods: {
    changeHidden () {
      this.hidden = !this.hidden
    },
    copyCode () {
      navigator.clipboard.writeText(this.userInfo.code)
        .then(() => {
          const alert = document.querySelector('.copy-msg')
          alert.style.display = 'block'
          setTimeout(() => {
            alert.style.display = 'none'
          }, 1500)
        })
    }
  }
}
</script>