"use strict";
import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';
import Vuelidate from 'vuelidate'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue);
Vue.use(Vuelidate)
Vue.use(VueRouter)

require('../css/styles.css');


var components = window.vueData.components;

var router = new VueRouter({
    mode: 'history',
    routes: window.vueData.routes,
    scrollBehavior (to, from, savedPosition) {
        return { x: 0, y: 0 }
    },
})

if (netid != undefined) {
    var _netID = netid
    Vue.mixin({
        data: function() {
            return {
                get netID() {
                    return _netID;
                }
            }
        },
        methods: {
            showErrorPage(errorData, redirectPage) {
                this.$router.push({ name: 'unrecoverable', params: {
                    errorHeading: errorData.statusText,
                    errorMessage: errorData.data[Object.keys(errorData.data)[0]],
                    errorCode: errorData.status,
                    tryAgainPage: redirectPage,
                }});
            }
        }
    })
    netid = undefined
}

export var vm = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    router,
    data() {
        return {
            scrollY: window.scrollY,
        }
    },
    components,
});

global.vm = vm
