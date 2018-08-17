"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUtensils, faChevronLeft, faCalendar, faClock, faMapMarkerAlt, faClipboardCheck } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUtensils)
library.add(faChevronLeft)
library.add(faCalendar)
library.add(faClock)
library.add(faMapMarkerAlt)
library.add(faClipboardCheck)
Vue.use(BootstrapVue);

Vue.component('font-awesome-icon', FontAwesomeIcon)

require('../css/styles.css');

import LabelledInput from './components/labelled-input.vue';
import FormCategory from './components/form-category.vue';
import AgreePop from './components/agreement-popup.vue';

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: function() {
        return {
            navVisible: false,
        }
    },
    components: {
        'labelled-input': LabelledInput,
        'form-category': FormCategory,
        'agreement-popup': AgreePop,
    },
});

window.onscroll = function () {
    app.navVisible = window.scrollY;
};
