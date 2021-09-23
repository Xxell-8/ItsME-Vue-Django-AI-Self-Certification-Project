<template>
  <div class="error">
    <div class="circle"></div>
    <div class="error-content f-column">
      <div class="code">404</div>
      <span class="msg">[ Page Not Found ]</span>
      <div class="msg-kr">요청하신 페이지를 찾을 수 없습니다.</div>
      <button
        class="btn btn-dark font-mont fw-500"
        @click="$router.go(-1)"
      >이전 페이지로 돌아가기</button>
    </div>
  </div>
</template>

<script>
import './error.scss'
export default {
  name: 'PageNotFound'
}
</script>

<style>

</style>