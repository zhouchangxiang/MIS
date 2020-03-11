import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/login'
import Index from '@/components/index'
import Error from '@/components/404'
import Config from '@/components/config'
import Home from '@/views/home'
import EfficiencyAnalysis from '@/views/energy/EfficiencyAnalysis'
import DataReport from '@/views/energy/DataReport'
import Areas from '@/views/energy/Areas'
import Organization from '@/views/SystemManage/Organization'
import Factory from '@/views/SystemManage/Factory'
import Role from '@/views/SystemManage/Role'
import Personnel from '@/views/SystemManage/Personnel'
import Calendar from '@/views/SystemManage/Calendar'
import Log from '@/views/SystemManage/Log'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'login',
      meta:{ title:'登录',isLogin: false},
      component: Login
    },
    {
      path:"/",
      name: 'index',
      meta:{ title:'好护士能源管理系统',isLogin: true},
      component: Index,
      redirect:'/home',
      children:[{
        path:'/home',
        name:'home',
        meta:{ title:'工作台',isLogin: true },
        component:Home
      },{
        path:'/EfficiencyAnalysis',
        name:'EfficiencyAnalysis',
        meta:{ title:'能效分析' },
        component:EfficiencyAnalysis
      },{
        path:'/DataReport',
        name:'DataReport',
        meta:{ title:'综合报表' },
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
      },{
        path:'/Factory',
        name:'Factory',
        meta:{ title:'厂区管理' },
        component:Factory
      },{
        path:'/Role',
        name:'Role',
        meta:{ title:'角色管理' },
        component:Role
      },{
        path:'/Personnel',
        name:'Personnel',
        meta:{ title:'人员管理' },
        component:Personnel
      },{
        path:'/Calendar',
        name:'Calendar',
        meta:{ title:'工厂日历' },
        component:Calendar
      },{
        path:'/Log',
        name:'Log',
        meta:{ title:'系统日志' },
        component:Log
      }]
    },
    {
      path:'/config',
      name:'Config',
      meta:{ title:'404' },
      component:Config
    },
    {
      path:'/404',
      name:'404',
      meta:{ title:'配置页' ,isLogin: false},
      component:Error
    }
  ]
})
