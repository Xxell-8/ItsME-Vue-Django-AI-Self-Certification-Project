<template>
  <div class="user-menu f-row-end">
    <div class="user-info" v-if="userInfo">
      <span>{{ userInfo.name }} {{ userInfo.fullname }}</span>님
    </div>
    <button
      class="btn btn-logout btn-outline fw-500"
      @click="onLogout"
    >로그아웃</button>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'UserNav',
  methods: {
    ...mapActions('accounts', ['onLogout'])
  },
  computed: {
    ...mapState('accounts', ['userInfo'])
  }
}
</script>