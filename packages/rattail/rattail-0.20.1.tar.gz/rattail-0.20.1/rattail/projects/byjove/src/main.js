import Vue from 'vue'
import router from './router'
import store from './store'
import vueResource from 'vue-resource'
import Cookie from 'js-cookie'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import App from './App.vue'
import {ByjovePlugin} from 'byjove'

Vue.config.productionTip = false

Vue.use(vueResource)

// the backend API will set a cookie for XSRF-TOKEN, which we will submit
// *back* to the backend API whenever we call it from then on.  we set this up
// globally so none of our API calls actually have to mess with it
Vue.http.interceptors.push((request, next) => {
    request.headers.set('X-XSRF-TOKEN', Cookie.get('XSRF-TOKEN'))
    next()
})

Vue.use(Buefy, {
    // use FontAwesome icon pack
    defaultIconPack: 'fas',
})

Vue.use(ByjovePlugin)

new Vue({
  router,
  store,
  render: function (h) { return h(App) }
}).$mount('#app')
