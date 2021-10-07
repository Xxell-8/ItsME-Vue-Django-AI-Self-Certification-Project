<template>
  <div class="link-form f-column">
    <!-- 0. 링크 이름 설정 -->
    <div class="input-box">
      <span class="label">회사명</span>
      <input 
        type="text"
        v-model="company"
        class="link-input"
        placeholder="고객에게 보여지는 회사명입니다."
        autocapitalize="off"
        autofocus
        required
      >
    </div>
    <!-- 1. 관리자 권한 설정-->
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

    <!-- 2. 만료 일시 설정 -->
    <div class="input-box">
      <span class="label">만료일시</span>
      <input v-model="expirationDate" type="datetime-local" class="link-input">
    </div>

    <!-- 3. 링크 이름 설정 -->
    <div class="input-box">
      <span class="label">링크 이름</span>
      <input 
        type="text"
        v-model="name"
        class="link-input"
        placeholder="미입력시, URL path를 이름으로 설정합니다."
        autocapitalize="off"
        autofocus
        required
      >
    </div>
  
    <div class="f-row">
      <!-- 4. 반복여부 -->
      <div class="ckeck-input">
        <input v-model="repeatable" type="checkbox" id="ch1" class="check-input" style="display: none;">
        <label for="ch1" class="check">
          <svg width="18px" height="18px" viewBox="0 0 18 18">
            <path d="M1,9 L1,3.5 C1,2 2,1 3.5,1 L14.5,1 C16,1 17,2 17,3.5 L17,14.5 C17,16 16,17 14.5,17 L3.5,17 C2,17 1,16 1,14.5 L1,9 Z"></path>
            <polyline points="1 9 7 14 15 4"></polyline>
          </svg>
        </label>
        <span>1회 인증 후 자동 종료</span>
      </div>
      <!-- 5. csv 파일 업로드 -->
      <div class="ckeck-input">
        <input v-model="hasData" type="checkbox" id="ch2" class="check-input" style="display: none;">
        <label class="check" for="input-file">
          <svg width="18px" height="18px" viewBox="0 0 18 18">
            <path d="M1,9 L1,3.5 C1,2 2,1 3.5,1 L14.5,1 C16,1 17,2 17,3.5 L17,14.5 C17,16 16,17 14.5,17 L3.5,17 C2,17 1,16 1,14.5 L1,9 Z"></path>
            <polyline points="1 9 7 14 15 4"></polyline>
          </svg>
        </label>
        <span>고객 데이터 등록</span>
        <span v-if="fileName" class="file-info">
          {{ fileName }}
          <i 
            class="fi fi-rr-cross-small"
            @click="onDeleteFile"
          ></i>
        </span>
        <span v-else class="descript">
          <i 
            class="icon fi fi-sr-interrogation"
          ></i>
          <div class="descript-content">
            고객 정보 업로드는 <span>csv 파일</span>로 가능하며,<br/>
            <span>이름</span>과 <span>생년월일</span>을 사전에 등록해<br/> 
            고객이 입력한 정보와 대조할 수 있습니다.<br/>
            정확한 정보 등록을 위해<br/>
            아래와 같이 각각의 <span>필드명</span>을<br/>
            <span>'name'</span>과 <span>'birth'</span>로 등록해주세요.
            <img 
              src="@/assets/image/dataExample.png" 
              alt=""
            >
          </div>
        </span>
        <input 
          id="input-file" 
          ref="file"
          type="file" 
          accept=".csv" 
          @change="onUploadCSV"
          style="display: none;"
        />
      </div>
    </div>
    <button
      class="btn btn-primary fw-900"
      @click="onCreateLink(linkData)"
    >링크 생성</button>
  </div>
</template>

<script>
import moment from 'moment'
import { mapState, mapActions } from 'vuex'
import Multiselect from '@vueform/multiselect'
import accountApi from '@/api/accounts.js'

export default {
  name: 'NewLinkForm',
  components: { 
    Multiselect,
  },
  data () {
    return {
      name: '',
      company: '',
      repeatable: true,
      hasData: false,
      expirationDate: moment().add(7, 'd').format('YYYY-MM-DDTHH:mm'),
      value: [],
      options: [],
      linkPath: null,
      fileName: null,
      fileInput: null,
      fileOutput: [],
    }
  },
  methods: {
    ...mapActions('partner', ['onCreateLink']),
    addViewer(event) {
      this.viewers.push(event.id)
    },
    removeViewer(event) {
      const index = this.viewers.indexOf(event.id)
      this.viewers.splice(index, 1)
    },
    makeLink() {
      let result = ''
      const char = 'abcdefghijklmnopqrstuvwxyz0123456789'
      for (let i = 0; i < 20; i++ ) {
        result += char.charAt(Math.floor(Math.random() * char.length))
      }
      this.linkPath = result
    },
    onUploadCSV (e) {
      const files = e.target.files
      if (!files.length)
        return;
      this.fileName = files[0].name
      this.createInput(files[0])
      this.$refs.file.value = ''
    },
    createInput(file) {
      var reader = new FileReader()
      reader.onload = () => {
        this.fileInput = reader.result
      }
      reader.readAsText(file, "EUC-KR")
    },
    csvToJson () {
      if (this.fileInput) {
        const lines = this.fileInput.trim().split('\n')
        const header = lines[0].split(',').map(key => key.trim())
        const output = lines.slice(1).map((line) => {
          const fields = line.split(',').map(key => key.trim())
          return Object.fromEntries(header.map((h, i) => [h, fields[i]]))
        })
        this.fileOutput = output
        this.hasData = true
      }
    },
    onDeleteFile () {
      this.hasData = false
      this.fileName = null
      this.fileInput = null
      this.fileOutput = []
    }
  },
  watch: {
    fileInput: function () {
      this.csvToJson()
    }
  },
  computed: {
    ...mapState('accounts', ['userInfo']),
    linkData () {
      return {
        path: this.linkPath,
        company: this.company,
        name: this.name,
        managers: this.value,
        repeatable: !this.repeatable,
        expired_at: this.expirationDate,
        customers: this.fileOutput
      }
    }
  },
  async created () {
    await accountApi.getUserList(this.userInfo.code)
      .then((res) => {
        // console.log(res)
        const users = res.data
        users.forEach((user) => {
          this.options.push({ 
            'label': user.fullname,
            'value': user.id
          })
        })
        this.value.push(this.userInfo.id)
      })
    this.company = this.userInfo.name
    this.makeLink()
  }
}
</script>

<style src="@vueform/multiselect/themes/default.css"></style>