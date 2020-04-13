import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/common/Login'
import Common from '@/components/common/Common'
import Home from '@/components/home/Home'
import Region from '@/components/region/Region'
import Efficiency from '@/components/efficiency/Efficiency'
import Report from '@/components/report/Report'

Vue.use(Router)

const router= new Router({
  routes: [
    {
      path: '/login',
      component: Login
    },
    {
      path: '/',
      component: Common,
      redirect:'/login',
      children:[
        {path:'/home',component:Home,meta:{requireAuth:true}},
        {path:'/region',component:Region,meta:{requireAuth:true}},
        {path:'/efficiency',component:Efficiency,meta:{requireAuth:true}},
        {path:'/report',component:Report,meta:{requireAuth:true}}
      ]
    }
  ]
})

// router.beforeEach((to,from,next)=>{
//   if (to.meta.requireAuth) {  // 判断该路由是否需要登录权限
//     if (localStorage.getItem('token')) {  // 获取当前的token是否存在
//       next();
//     } else {
//       alert('请先登录')
//       next('/login')
//     }
//   }
//   else { // 如果不需要权限校验，直接进入路由界面
//     if(localStorage.getItem('token')){
//       localStorage.removeItem('token')
//       next()
//     }
//     next();
//   }
// })

export default router