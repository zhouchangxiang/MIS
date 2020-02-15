import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/login'
import Index from '@/components/index'
import Error from '@/components/404'
import Home from '@/views/home'
import RealTimeData from '@/views/energy/RealTimeData'
import DataReport from '@/views/energy/DataReport'
import Organization from '@/views/SystemManage/Organization'
import Areas from '@/views/energy/Areas'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'login',
      meta:{ title:'登录' },
      component: Login
    },
    {
      path:"/",
      name: 'index',
      meta:{ title:'好护士能源管理系统'},
      component: Index,
      redirect:'/home',
      children:[{
        path:'/home',
        name:'home',
        meta:{ title:'工作台' },
        component:Home
      },{
        path:'/RealTimeData',
        name:'RealTimeData',
        meta:{ title:'实时数据' },
        component:RealTimeData
      },{
        path:'/DataReport',
        name:'DataReport',
        meta:{ title:'数据报表' },
        component:DataReport
      },{
        path:'/Areas',
        name:'Areas',
        meta:{ title:'区域展示' },
        component:Areas
      },{
        path:'/Organization',
        name:'Organization',
        meta:{ title:'组织架构' },
        component:Organization
      }]
    },
    {
      path:'/404',
      name:'404',
      meta:{ title:'404' },
      component:Error
    }
  ]
})
