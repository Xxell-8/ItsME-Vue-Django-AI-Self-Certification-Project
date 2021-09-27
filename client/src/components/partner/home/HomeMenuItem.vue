<template>
  <div class="menu-item f-column">
    <div class="subtitle">{{ menu.subtitle }}</div>
    <div class="title">{{ menu.title }}</div>
    <div v-html="menu.content" class="content"></div>
    <button
      class="btn btn-menu btn-primary fw-500"
      @click="$router.push({ name: menu.link })"
    >바로 가기</button>
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