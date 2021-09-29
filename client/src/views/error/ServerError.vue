<template>
  <div class="error">
    <div class="circle"></div>
    <div class="error-content f-column">
      <div class="code">500</div>
      <span class="msg">[ Interval Server Error ]</span>
      <div class="msg-kr">
        서버에 알 수 없는 오류가 발생했습니다.<br/>
        잠시후에 다시 시도해주세요.
      </div>
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
  name: 'ServerError'
}
</script>

<style>

</style>