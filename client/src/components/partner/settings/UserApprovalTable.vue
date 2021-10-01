<template>
  <tr>
    <td>{{ user.fullname }}</td>
    <td>{{ user.email }}</td>
    <td>{{ user.phone }}</td>
    <td>
      <span 
        class="btn-approval"
        @click="onApproveUser(user.id)"
      >
        가입 승인
      </span>
    </td>
  </tr>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'UserApprovalTable',
  props: {
    user: Object,
  },
  methods: {
    ...mapActions('accounts', ['onApproveUser'])
  }
}
</script>

<style>

</style>