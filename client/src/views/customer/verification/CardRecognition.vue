<template>
  <div class="card-recognition">
    <Leaflet v-if="isLoading" :message="message"/>
    <CardRecognitionCamera v-show="!isLoading"/>
  </div>
</template>

<script>
import './verification.scss'
import CardRecognitionCamera from '@/components/customer/verification/CardRecognitionCamera.vue'
import Leaflet from '@/components/customer/verification/Leaflet.vue'

export default {
  name: 'CardRecognition',
  components: {
    CardRecognitionCamera,
    Leaflet
  },
  props: {},
  data() {
    return {
      isLoading: true,
      message: {
        prev: '동작',
        next: '신분증',
      }
    }
  },
  mounted() {
    setTimeout(() => {this.isLoading = false}, 3000)
  }
}
</script>