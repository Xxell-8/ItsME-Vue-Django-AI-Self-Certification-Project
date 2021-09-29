<template>
  <div class="face-recognition">
    <FaceRecognitionCamera/>
  </div>
</template>

<script>
import './verification.scss'
import FaceRecognitionCamera from '@/components/customer/verification/FaceRecognitionCamera.vue'

export default {
  name: 'FaceRecognition',
  components: {
    FaceRecognitionCamera
  },
  props: {},
  data() {
    return {}
  }
}
</script>