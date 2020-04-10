import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/common/Login'
import Common from '@/components/common/Common'
import Home from '@/components/home/Home'
import Region from '@/components/region/Region'
import Efficiency from '@/components/efficiency/Efficiency'
import Report from '@/components/report/Report'

Vue.use(Router)


export default new Router({
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
