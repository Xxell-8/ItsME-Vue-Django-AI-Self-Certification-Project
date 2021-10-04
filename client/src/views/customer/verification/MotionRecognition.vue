<template>
  <div class="motion-recognition">
    <Leaflet v-if="isLoading" :message="message"/>
    <MotionRecognitionCamera v-show="!isLoading"/>
  </div>
</template>

<script>
import './verification.scss'
import MotionRecognitionCamera from '@/components/customer/verification/MotionRecognitionCamera.vue'
import Leaflet from '@/components/customer/verification/Leaflet.vue'

export default {
  name: 'MotionRecognition',
  components: {
    MotionRecognitionCamera,
    Leaflet
  },
  props: {},
  data() {
    return {
      isLoading: true,
      message: {
        prev: '얼굴',
        next: '동작',
      }
    }
  },
  mounted() {
    setTimeout(() => {this.isLoading = false}, 3000)
  }
}
</script>