<template>
  <div class="partners">
    <div class="circle-primary"></div>
    <PartnerNav/>
    <UserNav/>
    <div class="body-with-nav">
      <div class="chapter f-column-start t-white">
        <div class="subtitle">본인 인증 데이터</div>
        <div class="title">고객 정보 관리</div>
      </div>
      <div class="f-column-start links" v-if="linkList">
        <LinkListItem
          v-for="link in linkList"
          :key="link.id"
          :info="link"
        />
      </div>
    </div>
  </div>
</template>

<script>
import './linkList.scss'
import { mapState, mapActions } from 'vuex'
import PartnerNav from '@/components/partner/common/PartnerNav'
import UserNav from '@/components/partner/common/UserNav'
import LinkListItem from '@/components/partner/link/LinkListItem'

export default {
  name: 'LinkList',
  components: {
    PartnerNav,
    UserNav,
    LinkListItem
  },
  methods: {
    ...mapActions('partner', ['getLinkList'])
  },
  computed: {
    ...mapState('partner', ['linkList'])
  },
  created () {
    this.getLinkList()
  }
}
</script>