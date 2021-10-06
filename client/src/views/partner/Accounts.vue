<template>
  <div class="accounts">
    <img class="logo-back" src="@/assets/image/logo/white-lg.svg" alt="logo">
    <Login
      v-if="current === 'login'"
    />
    <Signup
      v-if="current === 'signup'"
    />
  </div>
</template>

<script>
import './accounts.scss'
import Login from '@/components/partner/accounts/Login'
import Signup from '@/components/partner/accounts/Signup'

export default {
  name: 'Accounts',
  data () {
    return {
      current: '',
    }
  },
  components: {
    Login,
    Signup
  },
  watch: {
    '$route' () {
      if (this.$route.name === 'Accounts') {
        if (this.$route.params.page === 'login' || this.$route.params.page === 'signup') {
          this.current = this.$route.params.page
        } else {
          this.$router.push('/404')
        }
      }

    }
  },
  created() {
    if (this.$route.params.page === 'login' || this.$route.params.page === 'signup') {
      this.current = this.$route.params.page
    } else {
      this.$router.push('/404')
    }
  }
}
</script>