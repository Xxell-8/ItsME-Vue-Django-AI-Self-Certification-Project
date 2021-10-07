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
      <div class="f-column-start links" v-if="linkList.length">
        <LinkListItem
          v-for="link in linkList"
          :key="link.id"
          :info="link"
        />
      </div>
      <div class="empty" v-else>
        관리 중인 링크가 없습니다.<br/>
        신규 링크를 생성하고 싶으시면,
        <span @click="$router.push({ name: 'NewLink' })">여기</span>를 눌러주세요.
      </div>
      <DeleteConfirm
        v-if="deleteModal"
      />
    </div>
  </div>
</template>

<script>
import './linkList.scss'
import { mapState, mapActions } from 'vuex'
import PartnerNav from '@/components/partner/common/PartnerNav'
import UserNav from '@/components/partner/common/UserNav'
import LinkListItem from '@/components/partner/link/LinkListItem'
import DeleteConfirm from '@/components/partner/link/DeleteConfirm'

export default {
  name: 'LinkList',
  components: {
    PartnerNav,
    UserNav,
    LinkListItem,
    DeleteConfirm
  },
  methods: {
    ...mapActions('partner', ['getLinkList'])
  },
  computed: {
    ...mapState('partner', ['linkList', 'deleteModal'])
  },
  created () {
    this.getLinkList()
  }
}
</script>