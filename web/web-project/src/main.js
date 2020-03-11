// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import axios from 'axios'
import qs from 'qs'
Vue.use(ElementUI)
import 'element-ui/lib/theme-chalk/index.css'
import './assets/common.css'
import Jqeury from './assets/script/jquery-3.3.1.min'
import 'font-awesome/css/font-awesome.min.css'
import moment from 'moment'
import VCharts from 'v-charts'
import FullCalendar from 'vue-full-calendar'
Vue.use(FullCalendar)
import Vue2OrgTree from 'vue2-org-tree'
Vue.use(Vue2OrgTree)
import store from './store'

Vue.config.productionTip = false
Vue.prototype.axios = axios
Vue.prototype.qs = qs
Vue.use(VCharts)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
router.beforeEach((to, from, next) => {
  if (to.meta.isLogin) {  //判断页面是否需要验证登录

  }else{
    next()
  }
})
