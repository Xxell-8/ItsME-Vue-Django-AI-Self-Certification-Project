<template>
  <div class="customers">
    <table>
      <thead>
        <tr>
          <th>No.</th>
          <th>
            이름
            <i class="fi fi-rr-arrow-small-down"></i>
          </th>
          <th>생년월일</th>
          <th>
            본인인증여부
            <i class="fi fi-rr-arrow-small-down"></i>
          </th>
          <th>인증 완료 시간</th>
        </tr>
      </thead>
      <tbody v-if="linkInfo.customers.length">
        <LinkDetailTableRow
          v-for="(customer, idx) in paginatedData"
          :key="idx"
          :customer="customer"
          :idx="idx + (currentPage - 1) * 10"
        />
      </tbody>
    </table>
    <div v-if="!linkInfo.customers.length" class="empty">
      인증을 완료한 고객이 없습니다.
    </div>

    <ul class="pagination" v-if="totalPage && totalPage > 1">
      <li
        :class="{ disabled: currentPage === 1 }"
        @click="changePage(currentPage - 1)"
      >&laquo;</li>
      <li
        :class="{ active: page === currentPage }"
        v-for="page in totalPage"
        :key="page"
        @click="changePage(page)"
      >
        {{ page }}
      </li>
      <li
        :class="{ disabled: currentPage === totalPage }"
        @click="changePage(currentPage + 1)"
      >&raquo;</li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import LinkDetailTableRow from './LinkDetailTableRow'
export default {
  name: 'LinkDetailTable',
  components: {
    LinkDetailTableRow
  },
  data () {
    return {
      currentPage: 1
    }
  },
  methods: {
    changePage(page) {
      this.currentPage = page
    }
  },
  computed: {
    ...mapState('partner', ['linkInfo']),
    paginatedData () {
      let start = (this.currentPage - 1) * 10
      let end = this.currentPage * 10
      return this.linkInfo.customers.slice(start, end)
    },
    totalPage () {
      const total = this.linkInfo.customers.length
      return Math.ceil(total/10)
    },
  }
}
</script>

<style>

</style>