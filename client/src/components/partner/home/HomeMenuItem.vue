<template>
  <div class="menu-item f-column">
    <div class="subtitle">{{ menu.subtitle }}</div>
    <div class="title">{{ menu.title }}</div>
    <div v-html="menu.content" class="content"></div>
    <button
      v-if="menu.link"
      class="btn btn-menu btn-primary fw-500"
      @click="$router.push({ name: menu.link })"
    >바로 가기</button>
    <button
      v-else
      class="btn btn-menu btn-disabled fw-500"
    >서비스 준비 중</button>
  </div>
</template>

<script>
export default {
  name: 'HomeMenuItem',
  props: {
    menu: Object
  }
}
</script>

<style>

</style>