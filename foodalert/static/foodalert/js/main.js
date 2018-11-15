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

Vue.component('font-awesome-icon', FontAwesomeIcon)

require('../css/styles.css');

import {store} from './store.js';

import LabelledInput from './components/labelled-input.vue';
import FormCategory from './components/form-category.vue';
import AgreePop from './components/agreement-popup.vue';
import PopContainer from './components/popup-container.vue';
import FormTemplate from './components/form-template.vue';
import FormController from './components/form-controller.vue';
import SignupTemplate from './components/signup-template.vue';
import UpdateTemplate from './components/update-template.vue';
import AuditTemplate from './components/audit-template.vue';
import EndedTemplate from './components/ended-template.vue';
import EndedController from './components/ended-controller.vue'
import GenericTemplate from './components/generic-template.vue';

var routes = [
    {
        path: "/",
        component: FormTemplate,
        name: "root",
        // children: [
        //     {path: "", component: FormTemplate, name: "form"},
        //     {path: "update", component: UpdateTemplate, name: "update"},
        // ],
    },
];

var router = new VueRouter({
    routes
})

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
    components: {
        'labelled-input': LabelledInput,
        'form-category': FormCategory,
        'agreement-popup': AgreePop,
        'popup-container': PopContainer,
        'form-template': FormTemplate,
        'form-controller': FormController,
        'signup-template': SignupTemplate,
        'update-template': UpdateTemplate,
        'audit-template': AuditTemplate,
        'ended-template': EndedTemplate,
        'ended-controller': EndedController,
        'generic-template': GenericTemplate,
    },
});

// router.push('/update');
