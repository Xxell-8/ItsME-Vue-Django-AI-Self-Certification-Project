<template>
  <div class="loading">
    <!-- 로딩을 위한 바운스 애니메이션 -->
    <div class="f-row">
      <div class="l-circle"></div>
      <div class="l-triangle"></div>
      <div class="l-square"></div>
    </div>
    <!-- message -->
    <div v-if="this.$route.name=='Result'" class="message t-white fw-700">
      <span><strong class="text-secondary">본인 인증</strong> 결과를 확인중입니다.</span>
      <span>잠시만 기다려주세요!</span>
    </div>
    <div v-if="this.$route.name=='FaceRecognition'" class="message t-white fw-700">
      <span><strong class="text-secondary">얼굴 인식</strong>을 준비중입니다.</span>
      <span>잠시만 기다려주세요!</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Loading',
  mounted() {
    console.log(this.$route.name)
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/style/_color.scss";
  .loading {
    width: 100vw;
    height: 100vh;
    background: $grey-dark;
    padding-top: 10rem;

    .l-circle {
      width: 2rem;
      height: 2rem;
      border-radius: 100%;
      border: 4px solid $primary;
      filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.3));
      animation: bounce-out-down 1.8s infinite;
      animation-delay: 0s;
    }
    .l-triangle {
      width: 0;
      height: 0;
      border-left: 1rem solid transparent;
      border-right: 1rem solid transparent;
      border-bottom: 1.7rem solid $light;
      filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.3));
      animation: bounce-out-down 1.8s infinite;
      animation-delay: 0.6s;
    }
    .l-square {
      width: 1.7rem;
      height: 1.7rem;
      border: 4px solid $secondary;
      filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.3));
      animation: bounce-out-down 1.8s infinite;
      animation-delay: 1.2s;
    }
  }

  @keyframes bounce-out-down {
    0% { transform: translateY(0); }
    20% {
      opacity: 1;
      transform: translateY(-20px);
    }
    100% {
      opacity: 0.3;
      transform: translateY(0);
    }
  }

  .message {
    display: flex;
    width: 100vw;
    margin-top: 3rem;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 1.5rem;
  }
    .text-secondary {
      color: $secondary
    }
</style>