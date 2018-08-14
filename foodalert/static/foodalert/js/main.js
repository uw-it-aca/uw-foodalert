"use strict";
import Vue from 'vue';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import HelloWorld from "./components/hello-world.vue";

require('../css/styles.css');

Vue.component('test-comp', {
    template: `<p> This is a test component`
});

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: function() {
        return {
            message: "Vue templating"
        }
    },
    components: {
        'hello-world': HelloWorld,
    },
});
