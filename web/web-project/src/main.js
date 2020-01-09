// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import axios from 'axios'
Vue.use(ElementUI)
import 'element-ui/lib/theme-chalk/index.css'
import Jqeury from './assets/script/jquery-3.3.1.min'
import 'font-awesome/css/font-awesome.min.css'
import moment from 'moment'
import VCharts from 'v-charts'

Vue.config.productionTip = false
Vue.prototype.axios = axios //设为Vue对象的方法
Vue.use(VCharts)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
