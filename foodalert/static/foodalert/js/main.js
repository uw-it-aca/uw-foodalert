"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUtensils, faChevronLeft } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUtensils)
library.add(faChevronLeft)
Vue.use(BootstrapVue);

Vue.component('font-awesome-icon', FontAwesomeIcon)

require('../css/styles.css');

import LabelledTextarea from './components/labelled-textarea.vue';
import FormCategory from './components/form-category.vue';
import AgreePop from './components/agreement-popup.vue';

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: function() {
        return {
        }
    },
    components: {
        'labelled-textarea': LabelledTextarea,
        'form-category': FormCategory,
        'agreement-popup': AgreePop,
    },
});
