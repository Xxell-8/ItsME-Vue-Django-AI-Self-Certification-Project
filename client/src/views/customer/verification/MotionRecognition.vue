<template>
  <div class="motion-recognition">
    <MotionRecognitionCamera/>
  </div>
</template>

<script>
import './verification.scss'
import MotionRecognitionCamera from '@/components/customer/verification/MotionRecognitionCamera.vue'

export default {
  name: 'MotionRecognition',
  components: {
    MotionRecognitionCamera
  },
  props: {},
  data() {
    return {}
  }
}
</script>