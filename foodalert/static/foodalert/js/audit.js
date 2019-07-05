import AuditTemplate from './components/audit-template.vue';
import AuditController from './components/audit-controller.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
    { path: "audit", component: AuditController },
]);

let rootPath = window.vueData.routes.find(obj => obj.path === "/");
rootPath.children.find(obj => obj.path === "audit").component = AuditController;
