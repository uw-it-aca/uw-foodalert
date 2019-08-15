'use strict';
import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuelidate from 'vuelidate';
import BootstrapVue from 'bootstrap-vue';

import '../css/custom.scss';

Vue.use(BootstrapVue);
Vue.use(Vuelidate);
Vue.use(VueRouter);

require('../css/styles.css');


const components = window.vueData.components;

const router = new VueRouter({
  mode: 'history',
  routes: window.vueData.routes,
  scrollBehavior(to, from, savedPosition) {
    return {x: 0, y: 0};
  },
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title;
  next();
});

if (netid != undefined) {
  const _netID = netid;
  Vue.mixin({
    data: function() {
      return {
        get netID() {
          return _netID;
        },
      };
    },
    methods: {
      showErrorPage(errorData, redirectPage) {
        this.$router.push({name: 'unrecoverable', params: {
          errorHeading: errorData.statusText,
          errorMessage: errorData.data[Object.keys(errorData.data)[0]],
          errorCode: errorData.status,
          tryAgainPage: redirectPage,
        }});
      },
    },
  });
  netid = undefined;
}

export const vm = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  router,
  data() {
    return {
      scrollY: window.scrollY,
    };
  },
  watch: {
    $route: function() {
      this.$nextTick(function() {
        setTimeout(() => {
          let focusTarget = 
            (this.$refs.appRouterView.$refs.foodalertAppRouter.$el !== undefined)
              ? this.$refs.appRouterView.$refs.foodalertAppRouter.$el
              : this.$refs.appRouterView.$el;
          let h1 = focusTarget.querySelector('h1');
          h1.setAttribute('tabindex', '-1');
          h1.focus();
          h1.removeAttribute('tabindex');
        }, 0);
      });
    }
  },
  components,
});

global.vm = vm;
