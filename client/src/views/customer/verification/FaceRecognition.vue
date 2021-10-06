<template>
  <div class="face-recognition">
    <Loading v-if="isLoading"/>
    <FaceRecognitionCamera v-show="!isLoading"/>
  </div>
</template>

<script>
import './verification.scss'
import FaceRecognitionCamera from '@/components/customer/verification/FaceRecognitionCamera.vue'
import Loading from '@/components/customer/verification/Loading.vue'

export default {
  name: 'FaceRecognition',
  components: {
    FaceRecognitionCamera,
    Loading
  },
  props: {},
  data() {
    return {
      isLoading: true,
    }
  },
  mounted() {
    setTimeout(() => {this.isLoading = false}, 3000)
  }
}
</script>