<template>
  <div class="form">
    <AccountFormLogin/>
  </div>
</template>

<script>
  import AccountFormLogin from './AccountFormLogin.vue'
  export default {
    name: 'AccountForm',
    components: {
      AccountFormLogin,
    }
  }
</script>