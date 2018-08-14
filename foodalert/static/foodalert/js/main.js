"use strict";
import Vue from 'vue';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

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
