import AuditTemplate from './components/audit-template.vue';
import AuditController from './components/audit-controller.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
    { path: "a/audit", component: AuditController },
]);

let rootPath = window.vueData.routes.find(obj => obj.path === "/a/");
function activatePage(name, page, title) {
    let route = rootPath.children.find(obj => obj.path === name)
    route.component = page
    route.meta.title = title
}

activatePage("audit", AuditController, "Audit Page")
