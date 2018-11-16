"use strict";
import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';
import Vuelidate from 'vuelidate'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
    faUtensils,
    faChevronLeft,
    faCalendar,
    faClock,
    faMapMarkerAlt,
    faClipboardCheck,
    faBell,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUtensils)
library.add(faChevronLeft)
library.add(faCalendar)
library.add(faClock)
library.add(faBell)
library.add(faMapMarkerAlt)
library.add(faClipboardCheck)
Vue.use(BootstrapVue);
Vue.use(Vuelidate)
Vue.use(VueRouter)

Vue.component('font-awesome-icon', FontAwesomeIcon)

require('../css/styles.css');

import {store} from './store.js';

import LabelledInput from './components/labelled-input.vue';
import GenericTemplate from './components/generic-template.vue';

export var routes = [
    {
        path: "/",
        component: GenericTemplate,
        name: "root",
        // children: [
        //     {path: "", component: FormTemplate, name: "form"},
        //     {path: "update", component: UpdateTemplate, name: "update"},
        // ],
    },
];

var router = new VueRouter({
    routes: routes,

})

export var components = {
    'labelled-input': LabelledInput,
    'generic-template': GenericTemplate,
}

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    store,
    router,
    data() {
        return {
            scrollY: window.scrollY,
        }
    },
    components,
});

