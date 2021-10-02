import { createStore } from 'vuex'
import partner from './modules/partner'
import customer from './modules/customer'
import accounts from './modules/accounts'
import verification from './modules/verification'
import createPersistedState from "vuex-persistedstate";

const store = createStore({
  plugins: [createPersistedState()],
  modules: {
    accounts,
    partner,
    customer,
    verification,
  }
})

export default store