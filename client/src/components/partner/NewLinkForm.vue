<template>
  <div class="link-form f-column">
    <!-- 1. 링크 이름 설정 -->
    <div class="input-box">
      <span class="label">링크 이름</span>
      <input 
        type="text"
        class="link-input"
        placeholder="미입력시, 기본 KEY를 이름으로 설정합니다."
        autocapitalize="off"
        autofocus
        required
      >
    </div>
    <!-- 2. 관리자 권한 설정-->
    <div class="input-box">
      <span class="label">관리자</span>
      <multiselect 
        v-model="value"
        mode="tags"
        :closeOnSelect="false"
        :searchable="true"
        :options=options
      ></multiselect>
    </div>

    <div class="f-row">
      <div>
        <input v-model="temp1" type="checkbox" id="ch1" class="check-input" style="display: none;">
        <label for="ch1" class="check">
          <svg width="18px" height="18px" viewBox="0 0 18 18">
            <path d="M1,9 L1,3.5 C1,2 2,1 3.5,1 L14.5,1 C16,1 17,2 17,3.5 L17,14.5 C17,16 16,17 14.5,17 L3.5,17 C2,17 1,16 1,14.5 L1,9 Z"></path>
            <polyline points="1 9 7 14 15 4"></polyline>
          </svg>
        </label>
        <span>Hello</span>
      </div>
      <div>
        <input type="checkbox" id="ch2" class="check-input" style="display: none;">
        <label for="ch2" class="check">
          <svg width="18px" height="18px" viewBox="0 0 18 18">
            <path d="M1,9 L1,3.5 C1,2 2,1 3.5,1 L14.5,1 C16,1 17,2 17,3.5 L17,14.5 C17,16 16,17 14.5,17 L3.5,17 C2,17 1,16 1,14.5 L1,9 Z"></path>
            <polyline points="1 9 7 14 15 4"></polyline>
          </svg>
        </label>
        <span>Hello</span>
      </div>
    </div>
  </div>
</template>

<script>
import Multiselect from '@vueform/multiselect'

export default {
  name: 'NewLinkForm',
  components: { 
    Multiselect
  },
  data () {
    return {
      temp1: false,
      value: [
        102345,
      ],
      options: [
        { label: '권기웅', value: 102333 },
        { label: '우만승', value: 102345 },
        { label: '이경민', value: 102356 },
        { label: '이세라', value: 102777 },
      ]
    }
  },
  methods: {
    addViewer(event) {
      this.viewers.push(event.id)
    },
    removeViewer(event) {
      const index = this.viewers.indexOf(event.id)
      this.viewers.splice(index, 1)
    },
  }
}
</script>

<style src="@vueform/multiselect/themes/default.css"></style>