
import Vue from 'vue';
import VueRouter from 'vue-router';
import BootstrapVue from 'bootstrap-vue';
import VueAnalytics from 'vue-analytics';

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
/* global logoutUrl*/
/* global twilioNumber*/
if (typeof netid !== 'undefined' && typeof logoutUrl !== 'undefined') {
  const _netID = netid;
  const _logoutUrl = logoutUrl;
  const _twilioNumber = twilioNumber

  Vue.mixin({
    data() {
      return {
        get netID() {
          return _netID;
        },
        get logoutUrl() {
          return _logoutUrl;
        },
        get twilioNumber() {
          return _twilioNumber;
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

const body = document.querySelector('#body');

const gaKey = body.dataset.gaKey;
const debugMode = body.dataset.debugMode;

// Configure VueAnalytics
Vue.use(VueAnalytics, {
  id: gaKey,
  router,
  set: [
    {field: 'anonymizeIp', value: true},
  ],
  debug: {
    enabled: debugMode,
    sendHitTask: !debugMode,
  },
});

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
