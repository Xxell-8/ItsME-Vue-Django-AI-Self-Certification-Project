<template>
  <div class="result">
    <Loading v-if="faceSimilarity===null && finished===false"/>
    <VerificationResult @finish="onFinish" v-show="faceSimilarity!==null && finished===false"/>
    <VerificationFinished v-if="finished===true" :name="customerName" />
  </div>
</template>

<script>
import './info.scss'
import Loading from '@/components/customer/verification/Loading.vue'
import VerificationResult from '@/components/customer/info/VerificationResult.vue'
import VerificationFinished from '@/components/customer/info/VerificationFinished.vue'

export default {
  name: 'Result',
  components: {
    Loading,
    VerificationResult,
    VerificationFinished,
  },
  props: {},
  data() {
    return {
      finished: false,
      customerName: null,
    }  
  },
  methods: {
    onFinish(name) {
      this.customerName = name;
      this.finished = true;
    }
  },
  computed: {
    faceSimilarity() {
      return this.$store.state.customer.faceSimilarity
    }
  },
}
</script>