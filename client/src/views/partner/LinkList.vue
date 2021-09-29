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
      <div class="f-column-start links">
        <LinkListItem
          v-for="(link, idx) in temp"
          :key="idx"
          :info="link"
        />
      </div>
    </div>
  </div>
</template>

<script>
import './linkList.scss'
import PartnerNav from '@/components/partner/common/PartnerNav'
import UserNav from '@/components/partner/common/UserNav'
import LinkListItem from '@/components/partner/LinkListItem'

export default {
  name: 'LinkList',
  components: {
    PartnerNav,
    UserNav,
    LinkListItem
  },
  data () {
    return {
      temp: [
        {
          id: 1,
          title: 'SW 역량 테스트 [Python 반]',
          total: 156,
          complete: 102,
          new: 38,
          created: '2021-09-15 10:00',
          expired: '2021-09-15 15:00',
        },
        {
          id: 2,
          title: 'SW 역량 테스트 [Java 반]',
          total: 248,
          complete: 206,
          new: 67,
          created: '2021-09-15 10:31',
          expired: '2021-09-15 15:30',
        },
        {
          id: 3,
          title: 'SW 역량 테스트 [C 반]',
          total: 43,
          complete: 32,
          new: 3,
          created: '2021-09-15 10:32',
          expired: '2021-09-15 15:30',
        },
      ]
    }
  }
}
</script>