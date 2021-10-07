<template>
  <div class="confirm">
    <div class="confirm-box">
      <i 
        class="fi fi-sr-cross-small exit-btn"
        @click="offDeleteModal"
      ></i>
      <div class="content">
        <div class="title">
          <span>{{ currentLink.name }}</span>을<br/>
          정말 삭제하시겠습니까?
        </div>
        <div class="descript">
          링크 삭제 시,
          그 안에 포함된 모든 고객 정보는
          자동으로 파기됩니다.
        </div>
      </div>
      <div class="btn-row">
        <button
          class="btn btn-grey"
          @click="offDeleteModal"
        >취소</button>
        <button
          class="btn btn-secondary"
          @click="onDeleteLink(currentLink.path)"
        >링크 삭제</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'DeleteConfirm',
  methods: {
    ...mapActions('partner', ['onDeleteLink', 'offDeleteModal'])
  },
  computed: {
    ...mapState('partner', ['currentLink'])
  }
}
</script>

<style>

</style>