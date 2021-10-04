<template>
  <div class="result">
    <Loading/>
  </div>
</template>

<script>
import './info.scss'
import Loading from '@/components/customer/verification/Loading.vue'

export default {
  name: 'Result',
  components: {
    Loading
  },
  props: {},
  data() {
    return {}  
  }
}
</script>