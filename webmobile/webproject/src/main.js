
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false
import './selfconfig/vantui.js'

import axios from 'axios'
Vue.prototype.$http=axios

import VLine from 'v-charts/lib/line.common'
import HisTogram from 'v-charts/lib/histogram.common'
import BMP from 'v-charts/lib/bmap.common'

Vue.component(VLine.name,VLine)
Vue.component(HisTogram.name,HisTogram)
Vue.component(BMP.name,BMP)


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
