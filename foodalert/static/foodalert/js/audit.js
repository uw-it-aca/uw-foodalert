import {activatePage} from './utils.js';
import AuditController from './components/audit-controller.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
  {path: 'a/audit', component: AuditController},
]);

const rootPath = window.vueData.routes.find((obj) => obj.path === '/a/');

activatePage(rootPath, 'audit', AuditController, 'Audit Page');
