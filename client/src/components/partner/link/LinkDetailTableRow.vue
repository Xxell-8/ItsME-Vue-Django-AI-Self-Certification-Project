<template>
  <tr>
    <td>{{ idx+1 }}</td>
    <td>{{ customer.name }}</td>
    <td>{{ birth }}</td>
    <td 
      v-if="customer.is_completed"
      class="emphasis"
    >인증 완료</td>
    <td v-else>미인증</td>
    <td v-if="customer.is_completed">{{ completedAt }}</td>
    <td v-else>-</td>
  </tr>
</template>

<script>
import moment from 'moment'
export default {
  name: 'LinkDetailTableRow',
  props: {
    customer: Object,
    idx: Number
  },
  computed: {
    birth () {
      if (this.customer.birth.includes('-')) {
        return this.customer.birth
      }
      return moment(this.customer.birth, 'YYYYMMDD').format('YYYY-MM-DD')
    },
    completedAt () {
      return moment(this.customer.completed_at).locale('ko').format('lll')
    }
  }
}
</script>

<style>

</style>