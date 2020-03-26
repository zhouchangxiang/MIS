
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false

import "./tools/vantui.js"

import axios from 'axios'
Vue.prototype.$http=axios
// import qs from 'qs'
// Vue.prototype.$qs=qs


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
