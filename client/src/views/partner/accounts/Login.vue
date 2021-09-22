<template>
  <div class="accounts">
    <img class="logo-back" src="@/assets/image/logo/white-lg.svg" alt="logo">
    <AccountForm/>
  </div>
</template>

<script>
import './accounts.scss'
import AccountForm from '@/components/partner/accounts/AccountForm.vue'

export default {
  name: 'Login',
  components: {
    AccountForm
  }
}
</script>