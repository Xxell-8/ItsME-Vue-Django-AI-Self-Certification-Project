<template>
  <div class="link-item f-row-between">
    <div class="content f-column-start">
      <span class="name">{{ info.name }}</span>
      <span class="status">
        총 
        <span>{{ info.total }}</span>
        명 중 
        <span>{{ info.complete_cnt }}</span>
        명이 본인 인증을 완료했습니다.
      </span>
      <div class="f-row date">
        <span>Created at<span class="info">{{ start }}</span></span>
        <span>Expired at<span class="info">{{ end }}</span></span>
      </div>
    </div>
    <button
      class="btn btn-detail btn-dark fw-500"
      @click="$router.push({ name: 'LinkDetail', params: { id: info.path }})"
    >상세 보기</button>
  </div>
</template>

<script>
import moment from 'moment'
export default {
  name: 'LinkListItem',
  props: {
    info: Object
  },
  methods: {

  },
  computed: {
    start () {
      return moment(this.info.created_at).format('YYYY-MM-DD HH:mm')
    },
    end () {
      return moment(this.info.expired_at).format('YYYY-MM-DD HH:mm')
    },
  }
}
</script>

<style>

</style>