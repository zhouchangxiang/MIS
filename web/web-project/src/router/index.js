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
import MaintainedBoard from '@/views/MaintainedTable/MaintainedBoard'
import MaintainedBatch from '@/views/MaintainedTable/MaintainedBatch'
import Organization from '@/views/SystemManage/Organization'
import Factory from '@/views/SystemManage/Factory'
import Role from '@/views/SystemManage/Role'
import Personnel from '@/views/SystemManage/Personnel'
import Calendar from '@/views/SystemManage/Calendar'
import SchedulingRules from '@/views/MaintainedTable/SchedulingRules'
import Log from '@/views/SystemManage/Log'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'login',
      meta:{ title:'登录'},
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
        meta:{ title:'工作台'},
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
        path:'/MaintainedBatch',
        name:'MaintainedBatch',
        meta:{ title:'批次维护表' },
        component:MaintainedBatch
      },{
        path:'/MaintainedBoard',
        name:'MaintainedBoard',
        meta:{ title:'综合维护表' },
        component:MaintainedBoard
      },{
        path:'/Areas',
        name:'Areas',
        meta:{ title:'区域展示' },
        component:Areas
      },{
        path:'/Organization',
        name:'Organization',
        meta:{ title:'系统管理' },
        component:Organization
      },{
        path:'/Factory',
        name:'Factory',
        meta:{ title:'系统管理' },
        component:Factory
      },{
        path:'/Role',
        name:'Role',
        meta:{ title:'系统管理' },
        component:Role
      },{
        path:'/Personnel',
        name:'Personnel',
        meta:{ title:'系统管理' },
        component:Personnel
      },{
        path:'/Calendar',
        name:'Calendar',
        meta:{ title:'系统管理' },
        component:Calendar
      },{
        path:'/SchedulingRules',
        name:'SchedulingRules',
        meta:{ title:'系统管理' },
        component:SchedulingRules
      },{
        path:'/Log',
        name:'Log',
        meta:{ title:'系统管理' },
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
