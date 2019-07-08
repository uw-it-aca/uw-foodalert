import GenericTemplate from './components/generic-template.vue';
import NotFoundTemplate from './components/not-found-template.vue';
import UnauthzTemplate from './components/unauthz-template.vue';
import TestTemplate from './pages/test-template.vue';
window.vueData = {};

window.vueData.routes = [
    {
        path: "/",
        component: GenericTemplate,
        children: [
            { path: "test-template", component: TestTemplate, name: "test-template" },
            { path: "a/audit", component: UnauthzTemplate, name: "a-audit" },
            { path: "h/welcome", component: UnauthzTemplate, name: "h-welcome" },
            { path: "h/food-service", component: UnauthzTemplate, name: "h-food-service" },
            { path: "h/categories", component: UnauthzTemplate, name: "h-categories" },
            { path: "h/responsibilities", component: UnauthzTemplate,name: "h-responsibilities" },
            { path: "h/need-permit", component: UnauthzTemplate, name: "h-need-permit" },
            { path: "h/form", component: UnauthzTemplate, name: "h-form" },
            { path: "h/update", component: UnauthzTemplate, name: "h-update", props: true },
            { path: "h/close", component: UnauthzTemplate, name: "h-close" },
            { path: "h/ended", component: UnauthzTemplate, name: "h-ended" },
            { path: "s/welcome", component: UnauthzTemplate, name: "s-welcome" },
            { path: "s/responsibilities", component: UnauthzTemplate, name: "s-responsibilities" },
            { path: "s/signup", component: UnauthzTemplate, name: "s-signup" },
            { path: "s/subscribed", component: UnauthzTemplate, name: "s-subscribed" },
        ],
    },
    {
        path: "*",
        component: NotFoundTemplate,
        name: "notfound"
    },
];
