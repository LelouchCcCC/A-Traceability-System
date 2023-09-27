import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import store from '../src/store'
Vue.config.productionTip = false
import axios from "axios";
import VueAxios from "vue-axios";
import MyCard from "@/components/template/MyCard";
Vue.component('my-card', MyCard)
axios.defaults.baseURL = 'http://127.0.0.1:5000';
Vue.use(VueAxios, axios)
import * as echarts from 'echarts'

Vue.prototype.$echarts = echarts
require('echarts/extension/bmap/bmap')
import uploader from "vue-simple-uploader";




Vue.use(uploader)
Vue.use(ElementUI);


router.beforeEach((to, from, next) => {
    store.commit('getToken')
    const token = store.state.user.token
    if (to.meta.requireAuth) {
        if (!token && to.name !== 'Login') {
            next({name: 'Login'})
        } else if (token && to.name === 'Login') {
            next({name: 'Index'})
        } else {
            next()
        }
    }
    next()
})


new Vue({
    render: h => h(App),
    router,
    store
}).$mount('#app')

