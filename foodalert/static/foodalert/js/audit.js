import AuditTemplate from './components/audit-template.vue';
import AuditController from './components/audit-controller.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
    { path: "a/audit", component: AuditController },
]);

let rootPath = window.vueData.routes.find(obj => obj.path === "/a/");
rootPath.children.find(obj => obj.path === "audit").component = AuditController;
