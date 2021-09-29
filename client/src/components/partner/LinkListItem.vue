<template>
  <div class="link-item f-row-between">
    <div class="content f-column-start">
      <span class="name">{{ info.title }}</span>
      <span class="status">
        총 
        <span>{{ info.total }}</span>
        명 중 
        <span>{{ info.complete }}</span>
        명이 본인 인증을 완료했습니다.
      </span>
      <div class="f-row date">
        <span>Created at<span class="info">{{ info.created }}</span></span>
        <span>Expired at<span class="info">{{ info.expired }}</span></span>
      </div>
    </div>
    <button
      class="btn btn-detail btn-dark fw-500"
      @click="$router.go(-1)"
    >상세 보기</button>
  </div>
</template>

<script>
export default {
  name: 'LinkListItem',
  props: {
    info: Object
  }
}
</script>

<style>

</style>