<template>
  <div class="f-column finished">
    <!-- title -->
    <div class="title-container">
      <img class="title-logo" src="@/assets/image/logo/white-lg.svg" alt="logo">
      <p class="title-text font-mont fw-900 t-white">It's Me!</p>
    </div>
    <!-- notification -->
    <div class="notification f-column">
      <p class="content-large fw-500 t-white"><strong class="t-green">본인인증</strong>이</p>
      <p class="content-large fw-500 t-white">완료되었습니다!</p>
      <p class="content fw-700 t-white mt-2">{{ name }}님의 소중한 개인정보는</p>
      <p class="content fw-700 t-white">즉시 파기됩니다.</p>
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