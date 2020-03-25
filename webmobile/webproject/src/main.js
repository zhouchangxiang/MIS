
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false

import { Button,Form,Field,Icon } from 'vant';

Vue.use(Button);
Vue.use(Form);
Vue.use(Field);
Vue.use(Icon );

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
