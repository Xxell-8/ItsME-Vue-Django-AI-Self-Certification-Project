import { createStore } from 'vuex'
import partner from './modules/partner'
import customer from './modules/customer'
import accounts from './modules/accounts'
import createPersistedState from "vuex-persistedstate";

const store = createStore({
  plugins: [createPersistedState()],
  modules: {
    accounts,
    partner,
    customer
  }
})

export default store