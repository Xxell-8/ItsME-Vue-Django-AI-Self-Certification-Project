<template>
  <div>
    <SignupCert v-if="!step" @next="step += 1"/>
    <SignupForm v-else-if="step === 1" @next="step += 1"/>
    <SignupComplete v-else-if="step === 2"/>
  </div>
</template>

<script>
import SignupCert from './SignupCert'
import SignupForm from './SignupForm'
import SignupComplete from './SignupComplete'

export default {
  name: 'Signup',
  components: {
    SignupCert,
    SignupForm,
    SignupComplete
  },
  data () {
    return {
      step: 0
    }
  },
}
</script>