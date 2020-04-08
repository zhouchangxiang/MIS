
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false
import './selfconfig/vantui.js'

import axios from 'axios'
Vue.prototype.$http=axios

import './assets/css/base.css'


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
