<template>
  <div class="f-column">
    <!-- title -->
    <img class="logo-back" src="@/assets/image/logo/white-lg.svg" alt="logo">
    <p class="title-big font-mont fw-900 t-white">It's Me!</p>
    <!-- notification -->
    <div class="notification f-column">
      <div class="content-box">
        <span class="content fw-700 t-white"><strong>본인인증</strong>이</span>
        <span class="content fw-700 t-white">완료되었습니다.</span>
        <span class="content fw-700 t-white">{{ name }}님의 소중한 개인정보는</span>
        <span class="content fw-700 t-white">즉시 파기됩니다.</span>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'VerificationFinished',
  props: {
    name: String,
  },
  data() {
    return {}  
  },
}
</script>