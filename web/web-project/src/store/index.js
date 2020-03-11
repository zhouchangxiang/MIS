import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);
export default new Vuex.Store({
  // 创建基本状态
  state: {
    WorkNumber:null,
    LoginStatus: false
  },
  // 创建改变状态的方法
  mutations: {
    handleUser:(state,user) =>{
      if(user){
        state.WorkNumber = user;
        state.LoginStatus = true;
      }else{
        sessionStorage.setItem('WorkNumber', null)
        state.WorkNumber = null
        state.LoginStatus = false;
      }
    }
  },
  actions: {
    setUser ({commit},user) {
      commit('handleUser',user)
    }
  },
  getters:{
    WorkNumber: state => state.WorkNumber,
    LoginStatus: state => state.LoginStatus
  }
});
