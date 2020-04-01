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
        {path:'/home',component:Home},
        {path:'/region',component:Region},
        {path:'/efficiency',component:Efficiency},
        {path:'/report',component:Report}
      ]
    }
  ]
})