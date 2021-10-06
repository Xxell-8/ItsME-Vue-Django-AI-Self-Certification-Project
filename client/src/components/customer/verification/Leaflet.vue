<template>
  <div class="leaflet">
    <!-- 성공 애니메이션 -->
    <div>
      <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
        <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none" />
        <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" />
      </svg>
    </div>
    <!-- message -->
    <div class="message">
      <span class="t-white fw-700"><strong class="text-secondary">{{ message.prev }}</strong> 인식이 완료되었습니다!</span>
      <span class="t-white fw-700"><strong class="text-secondary">{{ message.next }}</strong> 인식을 준비중입니다.</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Leaflet',
  props: {
    message: Object
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/style/_color.scss";
  .leaflet {
    width: 100vw;
    height: 100vh;
    background: $grey-dark;
    padding-top: 10rem;

    .checkmark {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        display: block;
        stroke-width: 3;
        stroke: $primary;
        stroke-miterlimit: 10;
        box-shadow: inset 0px 0px 0px $primary;
        animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
        position:relative;
        top: 5px;
        right: 5px;
        margin: 0 auto;
    }
    .checkmark__circle {
        stroke-dasharray: 166;
        stroke-dashoffset: 166;
        stroke-width: 3;
        stroke-miterlimit: 10;
        stroke: $primary;
        fill: $grey-dark;
        animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
    
    }

    .checkmark__check {
        transform-origin: 50% 50%;
        stroke-dasharray: 48;
        stroke-dashoffset: 48;
        animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
    }
  }


@keyframes stroke {
    100% {
        stroke-dashoffset: 0;
    }
}

@keyframes scale {
    0%, 100% {
        transform: none;
    }

    50% {
        transform: scale3d(1.1, 1.1, 1);
    }
}

@keyframes fill {
    100% {
        box-shadow: inset 0px 0px 0px 30px $primary;
    }
}

.message {
  display: flex;
  width: 100vw;
  margin-top: 1.5rem;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
}
  .text-secondary {
    color: $secondary
  }
</style>