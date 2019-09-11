import {activatePage} from './utils.js';
import AuditTemplate from './components/audit-template.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
  {path: 'a/audit', component: AuditTemplate},
]);

const rootPath = window.vueData.routes.find((obj) => obj.path === '/a/');

activatePage(rootPath, 'audit', AuditTemplate, 'Audit Page');
