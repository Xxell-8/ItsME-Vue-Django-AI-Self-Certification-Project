<template>
  <div class="approval-box shadow">
    <div class="ap-header">
      <div class="setting-name">
        <span>가입 승인 요청</span>
      </div>
      <button
        v-if="unapprovedUsers.length"
        class="btn btn-primary"
        @click="onApproveAll"
      >전체 승인</button>
    </div>
    <table>
      <thead>
        <tr>
          <th>이름</th>
          <th>이메일</th>
          <th>연락처</th>
          <th>인증 완료 시간</th>
        </tr>
      </thead>
      <tbody v-if="unapprovedUsers.length">
        <UserApprovalTable
          v-for="(user, idx) in unapprovedUsers"
          :key="idx"
          :user="user"
          :idx="idx"
        />
      </tbody>
    </table>
    <div v-if="!unapprovedUsers.length" class="empty">
      가입 승인을 요청한 사용자가 없습니다.
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import UserApprovalTable from './UserApprovalTable'

export default {
  name: 'UserApproval',
  components: {
    UserApprovalTable
  },
  methods: {
    ...mapActions('accounts', ['getUnapprovedUsers', 'onApproveUser']),
    onApproveAll () {
      this.unapprovedUsers.forEach((user) => {
        console.log(user.id)
        this.onApproveUser(user.id)
      })
    }
  },
  computed: {
    ...mapState('accounts', ['unapprovedUsers']),
  },
  created () {
    this.getUnapprovedUsers()
  }
}
</script>