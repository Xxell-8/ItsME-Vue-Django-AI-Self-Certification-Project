<template>
  <div class="f-row-left">
    <HomeMenuItem
      v-for="(menu, idx) in homeMenu"
      :key="idx"
      :menu="menu"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import HomeMenuItem from './HomeMenuItem'

export default {
  name: 'HomeMenu',
  components: {
    HomeMenuItem
  },
  computed: {
    ...mapState('partner', ['homeMenu'])
  }
}
</script>

<style>

</style>