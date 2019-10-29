import {activatePage} from './utils.js';
import AuditLog from './pages/audit/audit-page.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
  {path: 'a/audit', component: AuditLog},
]);

const rootPath = window.vueData.routes.find((obj) => obj.path === '/a/');

activatePage(rootPath, 'audit', AuditLog, 'Audit Page');
