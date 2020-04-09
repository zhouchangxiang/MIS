import Vue from 'vue'
import App from './App'
import router from './router'

import store from './store/index'

Vue.config.productionTip = false
import './selfconfig/vantui.js'

import http from './selfconfig/http'
Vue.prototype.$http=http

import qs from 'qs'
Vue.prototype.$qs=qs

import './assets/css/base.css'

router.beforeEach((to,from,next)=>{
  if (to.meta.requireAuth) {  // 判断该路由是否需要登录权限
    if (localStorage.getItem('token')) {  // 获取当前的token是否存在
      next();
    } else {
      alert('请先登录')
      next('/login')
    }
  }
  else { // 如果不需要权限校验，直接进入路由界面
    if(localStorage.getItem('token')){
      localStorage.removeItem('token')
      next()
    }
    next();
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
