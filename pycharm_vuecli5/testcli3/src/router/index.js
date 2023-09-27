const Judge = () => import('@/components/content/chaxun/Judge')
const City = () => import('@/components/content/city/MainCity')
const Index = () => import('@/components/content/Index')
const Main = () => import('@/components/content/city/MainCity2')
const Mag = () => import('@/components/content/manager/Mag')


//配置路由信息
import Vue from "vue";
//配置路由信息
import VueRouter from "vue-router";
// const Home = () => import()
//通过安装插件，传入路由对象
Vue.use(VueRouter)


//创建VueRouter对象
const routes = [
    {
        path: '/',
        redirect: to => {
            return '/index'
        },
        component: () => import('../components/common/newGong'),
        meta: {  // 加一个自定义obj
            requireAuth: true   // 参数 true 代表需要登陆才能进入 A
        },
        children: [
            {
                path: '/index',
                component: Index,
                name: 'Index',
                meta: {  // 加一个自定义obj
                    requireAuth: true   // 参数 true 代表需要登陆才能进入 A
                },
                // children:[
                //     {
                //         path: 'msg',
                //         component:Msg,
                //     },
                //     {
                //         path:'news',
                //         component:News,
                //     },
                // ],
            },
            {
                path: '/jug',
                name: 'Jug',
                component: Judge,
            },
            {
                path: '/city/:cityname',
                component: City,
                meta: {  // 加一个自定义obj
                    requireAuth: true   // 参数 true 代表需要登陆才能进入 A
                },
            },
            {
                path: '/main',
                component: Main,
                name: 'Main',
                meta: {  // 加一个自定义obj
                    requireAuth: true   // 参数 true 代表需要登陆才能进入 A
                },
            },
            {
                path: '/mag',
                component: Mag,
                name: 'Mag',
                meta: {  // 加一个自定义obj
                    requireAuth: true   // 参数 true 代表需要登陆才能进入 A
                },
            },
            {
                path: '/message',
                name: 'Message',
                meta: {
                    requireAuth: true
                },
                component: () => import('../components/content/manager/Message')
            },
            {
                path: '/add-web',
                name: 'AddWeb',
                meta: {
                    requireAuth: true
                },
                component: () => import('../components/content/manager/AddWeb')
            },
            {
                path: '/bulletin',
                name: 'Bulletin',
                meta: {
                    requireAuth: true
                },
                component: () => import('../components/content/manager/Bulletin')
            },
            {
                path: '/sql',
                name: 'Sql',
                meta: {
                    requireAuth: true
                },
                component: () => import('../components/content/manager/Sql')
            },
            {
                path: '/admin',
                name: 'Admin',
                meta: {
                    requireAuth: true
                },
                component: () => import('../components/content/manager/AdminAdd')
            },
            {
                path: '/rizhi',
                name: 'RiZhi',
                meta: {
                    requireAuth: true
                },
                component: () => import('../components/content/manager/riZhi')
            }
        ]
    },


    {
        path: '/login',
        name: 'Login',
        meta: {  // 加一个自定义obj
            requireAuth: true   // 参数 true 代表需要登陆才能进入 A
        },
        component: () => import('../components/Login')
    },

    // {
    //     path:'/left',
    //     name:'Left',
    //     component:()=>import('../components/common/Left')
    // }
    // {
    //     path: '/login',
    //     component:Login,
    // }
]
const router = new VueRouter({
    routes,
    mode: 'history',
    linkActiveClass: 'active'
})

//将router对象传入vue实例中
export default router

