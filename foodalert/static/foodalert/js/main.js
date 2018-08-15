"use strict";
import Vue from 'vue';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUtensils } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUtensils)

Vue.component('font-awesome-icon', FontAwesomeIcon)

require('../css/styles.css');

import LabelledTextarea from './components/labelled-textarea.vue';
import FormCategory from './components/form-category.vue';

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
    },
});
