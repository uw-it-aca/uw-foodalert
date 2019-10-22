
import Vue from 'vue';
import VueRouter from 'vue-router';
import BootstrapVue from 'bootstrap-vue';

import '../css/custom.scss';

Vue.use(BootstrapVue);
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

/* global netid*/
if (typeof netid !== 'undefined' && typeof logoutUrl !== 'undefined') {
  const _netID = netid;
  const _logoutUrl = logoutUrl;

  Vue.mixin({
    data() {
      return {
        get netID() {
          return _netID;
        },
        get logoutUrl() {
          return _logoutUrl;
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
      stopOnButtonClick(evt) {
        if (evt.target.tagName === 'BUTTON') {
          evt.preventDefault();
        }
      },
    },
  });
}

export const vm = new Vue({
  render: (createElement) => createElement('router-view'),
  router,
  data() {
    return {
      scrollY: window.scrollY,
    };
  },
  components,
}).$mount('#app');

global.vm = vm;
