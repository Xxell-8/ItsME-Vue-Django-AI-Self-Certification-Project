<template>
  <div class="loading">
    <!-- 로딩을 위한 바운스 애니메이션 -->
    <div class="f-row">
      <div class="l-circle"></div>
      <div class="l-triangle"></div>
      <div class="l-square"></div>
    </div>

    <!-- 코너 테두리 사각형 -->
    <div class="corner">
      <div class="top-left"></div>
      <div class="top-right"></div>
      <div class="bottom-left"></div>
      <div class="bottom-right"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Loading'
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

  .corner {
    width: 90vw;
    height: 50vw;
    margin: 1rem auto;
    position: relative;
    
    div {
      width: 2rem;
      height: 2rem;
      position: absolute;
      border-color: rgba($secondary, 0.7);
      border-style: solid;

      &.top-left {
        top: 0;
        left: 0;
        border-width: 4px 0 0 4px;
      }
      &.top-right {
        top: 0;
        right: 0;
        border-width: 4px 4px 0 0;
      }
      &.bottom-left {
        bottom: 0;
        left: 0;
        border-width: 0 0 4px 4px;
      }
      &.bottom-right {
        bottom: 0;
        right: 0;
        border-width: 0 4px 4px 0;
      }
    }
  }

</style>