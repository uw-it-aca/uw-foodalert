import AuditTemplate from './components/audit-template.vue';
import AuditController from './components/audit-controller.vue';
import * as main from './main.js';

main.components['audit-template'] = AuditTemplate;
main.components['audit-controller'] = AuditController;

main.routes[0].children = main.routes[0].children.concat([
    { path: "audit", component: AuditController, name: "audit" }
]);

//main.router.addRoutes(main.routes);
