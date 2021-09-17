import { createStore } from 'vuex'
import partner from './modules/partner'
import customer from './modules/customer'
import createPersistedState from "vuex-persistedstate";

const store = createStore({
  plugins: [createPersistedState()],
  modules: {
    partner,
    customer
  }
})

export default store