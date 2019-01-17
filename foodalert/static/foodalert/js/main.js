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
    routes: window.vueData.routes,
})

export var app = new Vue({
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
