<template>
  <div class="partners">
    <div class="circle-primary"></div>
    <PartnerNav/>
    <UserNav/>
    <div class="body-with-nav">
      <div class="chapter f-column-start t-white">
        <div class="subtitle">본인 인증 서비스</div>
        <div class="title">신규 링크 생성</div>
      </div>
      <NewLinkForm/>
      <CreateSuccess
        v-if="successModal"
      />
    </div>
  </div>
</template>

<script>
import './newLink.scss'
import { mapState } from 'vuex'
import PartnerNav from '@/components/partner/common/PartnerNav'
import UserNav from '@/components/partner/common/UserNav'
import NewLinkForm from '@/components/partner/newLink/NewLinkForm'
import CreateSuccess from '@/components/partner/newLink/CreateSuccess'

export default {
  name: 'NewLink',
  components: {
    PartnerNav,
    UserNav,
    NewLinkForm,
    CreateSuccess
  },
  computed: {
    ...mapState('partner', ['successModal'])
  }
}
</script>

<style>

</style>