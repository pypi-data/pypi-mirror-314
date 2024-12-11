import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import {Customers, Customer} from './views/customers'
import {Products, Product} from './views/products'
// import {OrderingBatches, OrderingBatch, OrderingBatchRow} from './views/ordering'
// import {ReceivingBatches, ReceivingBatch, ReceivingBatchRow, ReceivingBatchRowReceive} from './views/receiving'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/login',
            name: 'login',
            component: Login
        },
        {
            path: '/about',
            name: 'about',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: function () {
                return import(/* webpackChunkName: "about" */ './views/About.vue')
            }
        },

        //////////////////////////////
        // Customers
        //////////////////////////////
        {
            path: '/customers/',
            name: 'customers',
            component: Customers
        },
        {
            path: '/customers/new',
            name: 'customers.new',
            component: Customer,
            props: {mode: 'creating'},
        },
        {
            path: '/customers/:uuid',
            name: 'customers.view',
            component: Customer,
            props: {mode: 'viewing'},
        },
        {
            path: '/customers/:uuid/edit',
            name: 'customers.edit',
            component: Customer,
            props: {mode: 'editing'},
        },

        //////////////////////////////
        // Products
        //////////////////////////////
        {
            path: '/products/',
            name: 'products',
            component: Products,
        },
        {
            path: '/products/new',
            name: 'products.new',
            component: Product,
            props: {mode: 'creating'},
        },
        {
            path: '/products/:uuid',
            name: 'products.view',
            component: Product,
            props: {mode: 'viewing'},
        },
        {
            path: '/products/:uuid/edit',
            name: 'products.edit',
            component: Product,
            props: {mode: 'editing'},
        },

        /*

        //////////////////////////////
        // Ordering
        //////////////////////////////
        {
            path: '/ordering/',
            name: 'ordering',
            component: OrderingBatches,
        },
        {
            path: '/ordering/new',
            name: 'ordering.new',
            component: OrderingBatch,
            props: {mode: 'creating'},
        },
        {
            path: '/ordering/:uuid',
            name: 'ordering.view',
            component: OrderingBatch,
            props: {mode: 'viewing'},
        },
        {
            path: '/ordering/:uuid/edit',
            name: 'ordering.edit',
            component: OrderingBatch,
            props: {mode: 'editing'},
        },
        {
            path: '/ordering/:uuid/execute',
            name: 'ordering.execute',
            component: OrderingBatch,
            props: {mode: 'executing'},
        },
        {
            path: '/ordering/rows/:uuid',
            name: 'ordering.rows.view',
            component: OrderingBatchRow,
            props: {mode: 'viewing'},
        },
        {
            path: '/ordering/rows/:uuid/edit',
            name: 'ordering.rows.edit',
            component: OrderingBatchRow,
            props: {mode: 'editing'},
        },

        //////////////////////////////
        // Receiving
        //////////////////////////////
        {
            path: '/receiving/',
            name: 'receiving',
            component: ReceivingBatches,
        },
        {
            path: '/receiving/new',
            name: 'receiving.new',
            component: ReceivingBatch,
            props: {mode: 'creating'},
        },
        {
            path: '/receiving/:uuid',
            name: 'receiving.view',
            component: ReceivingBatch,
            props: {mode: 'viewing'},
        },
        {
            path: '/receiving/:uuid/edit',
            name: 'receiving.edit',
            component: ReceivingBatch,
            props: {mode: 'editing'},
        },
        {
            path: '/receiving/rows/:uuid',
            name: 'receiving.rows.view',
            component: ReceivingBatchRow,
            props: {mode: 'viewing'},
        },
        // {
        //     path: '/receiving/rows/:uuid/edit',
        //     name: 'receiving.rows.view',
        //     component: ReceivingBatchRow,
        //     props: {mode: 'editing'},
        // },
        {
            path: '/receiving/rows/:uuid/receive',
            name: 'receiving.rows.receive',
            component: ReceivingBatchRowReceive,
        },
        {
            path: '/receiving/:uuid/execute',
            name: 'receiving.execute',
            component: ReceivingBatch,
            props: {mode: 'executing'},
        },

        */

    ],
    scrollBehavior (to, from, savedPosition) {
        // always scroll to top of new page when navigating
        return {x: 0, y: 0}
    },
})
