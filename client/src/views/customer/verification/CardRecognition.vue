<template>
  <div class="card-recognition">
    <CardRecognitionCamera/>
  </div>
</template>

<script>
import './verification.scss'
import CardRecognitionCamera from '@/components/customer/verification/CardRecognitionCamera.vue'

export default {
  name: 'CardRecognition',
  components: {
    CardRecognitionCamera
  },
  props: {},
  data() {
    return {}
  }
}
</script>