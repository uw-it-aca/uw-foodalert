import AuditTemplate from './components/audit-template.vue';
import AuditController from './components/audit-controller.vue';

Object.assign(window.vueData.components, {
    "audit-template" : AuditTemplate,
    "audit-controller" : AuditController
});

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
    { path: "audit", component: AuditController },
]);
