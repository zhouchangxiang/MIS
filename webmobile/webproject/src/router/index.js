import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)


export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
// Router.beforeEach((to, from, next) => {
//   if(to.path==="/login") return next()
//   if(!token) return next('/login')
//   next()
 
//  })
