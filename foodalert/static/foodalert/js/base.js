import GenericTemplate from './components/generic-template.vue';
import NotFoundTemplate from './components/not-found-template.vue';
import UnauthzTemplate from './components/unauthz-template.vue';
import UnrecoverablePage from './pages/unrecoverable-page.vue';
import TestTemplate from './pages/test-template.vue';
window.vueData = {};

window.vueData.routes = [
  {
    path: '/a/',
    component: GenericTemplate,
    redirect: {name: 'a-audit'},
    children: [
      {
        path: 'audit',
        component: UnauthzTemplate,
        name: 'a-audit',
        meta: {title: 'Unauthorized Page'},
      },
    ],
  },
  {
    path: '/h/',
    component: GenericTemplate,
    redirect: {name: 'h-welcome'},
    children: [
      {
        path: 'welcome',
        component: UnauthzTemplate,
        name: 'h-welcome',
        meta: {title: 'Unauthorized Page'},
      },
      {
        path: 'food-service',
        component: UnauthzTemplate,
        name: 'h-food-service',
        meta: {title: 'Unauthorized Page'},
      },
      {
        path: 'categories',
        component: UnauthzTemplate,
        name: 'h-categories',
        meta: {title: 'Unauthorized Page'},
      },
      {
        path: 'responsibilities',
        component: UnauthzTemplate,
        name: 'h-responsibilities',
        meta: {title: 'Unauthorized Page'},
        props: true,
      },
      {
        path: 'need-permit',
        component: UnauthzTemplate,
        name: 'h-need-permit',
        meta: {title: 'Unauthorized Page'},
      },
      {
        path: 'form',
        component: UnauthzTemplate,
        name: 'h-form',
        meta: {title: 'Unauthorized Page'},
        props: true,
      },
      {
        path: 'update',
        component: UnauthzTemplate,
        name: 'h-update',
        meta: {title: 'Unauthorized Page'},
        props: true,
      },
      {
        path: 'close',
        component: UnauthzTemplate,
        name: 'h-close',
        meta: {title: 'Unauthorized Page'},
      },
      {
        path: 'ended',
        component: UnauthzTemplate,
        name: 'h-ended',
        meta: {title: 'Unauthorized Page'},
      },
    ],
  },
  {
    path: '/s/',
    component: GenericTemplate,
    redirect: {name: 's-welcome'},
    children: [
      {
        path: 'welcome',
        component: UnauthzTemplate,
        name: 's-welcome',
        meta: {title: 'Unauthorized Page'},
      },
      {
        path: 'responsibilities',
        component: UnauthzTemplate,
        name: 's-responsibilities',
        meta: {title: 'Unauthorized Page'},
      },
      {
        path: 'notifications',
        component: UnauthzTemplate,
        name: 's-notifications',
        meta: {title: 'Unauthorized Page'},
        props: true,
      },
      {
        path: 'signup',
        component: UnauthzTemplate,
        name: 's-signup',
        meta: {title: 'Unauthorized Page'},
      },
      {
        path: 'subscribed',
        component: UnauthzTemplate,
        name: 's-subscribed',
        meta: {title: 'Unauthorized Page'},
      },
    ],
  },
  {
    path: '/',
    component: GenericTemplate,
    redirect: () => {
      window.location.replace('http://www.washington.edu/anyhungryhusky/');
    },
    children: [
      {
        path: 'test-template',
        component: TestTemplate,
        name: 'test-template',
      },
      {
        path: 'unrecoverable',
        component: UnrecoverablePage,
        name: 'unrecoverable',
        meta: {title: 'There was an unrecoverable error'},
        props: true,
      },
    ],
  },
  {
    path: '*',
    component: NotFoundTemplate,
    name: 'notfound',
    meta: {title: 'Page not found'},
  },
];
