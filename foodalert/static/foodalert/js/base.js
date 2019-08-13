import GenericTemplate from './components/generic-template.vue';
import NotFoundTemplate from './components/not-found-template.vue';
import UnauthzTemplate from './components/unauthz-template.vue';
import UnrecoverablePage from './pages/unrecoverable-page.vue';
import TestTemplate from './pages/test-template.vue';
window.vueData = {};

window.vueData.routes = [
    {
        path: "/a/",
        component: GenericTemplate,
        children: [
            { path: "audit", component: UnauthzTemplate, name: "a-audit" },
        ],
    },
    {
        path: "/h/",
        component: GenericTemplate,
        redirect: { name: "h-welcome" },
        children: [
            { path: "welcome", component: UnauthzTemplate, name: "h-welcome" },
            { path: "food-service", component: UnauthzTemplate, name: "h-food-service" },
            { path: "categories", component: UnauthzTemplate, name: "h-categories" },
            { path: "responsibilities", component: UnauthzTemplate,name: "h-responsibilities" },
            { path: "need-permit", component: UnauthzTemplate, name: "h-need-permit" },
            { path: "form", component: UnauthzTemplate, name: "h-form" },
            { path: "update", component: UnauthzTemplate, name: "h-update", props: true },
            { path: "close", component: UnauthzTemplate, name: "h-close" },
            { path: "ended", component: UnauthzTemplate, name: "h-ended" },
        ],
    },
    {
        path: "/s/",
        component: GenericTemplate,
        redirect: { name: "s-welcome" },
        children: [
            { path: "welcome", component: UnauthzTemplate, name: "s-welcome" },
            { path: "responsibilities", component: UnauthzTemplate, name: "s-responsibilities" },
            { path: "notifications", component: UnauthzTemplate, name: "s-notifications" },
            { path: "signup", component: UnauthzTemplate, name: "s-signup" },
            { path: "subscribed", component: UnauthzTemplate, name: "s-subscribed" },
        ],
    },
    {
        path: "/",
        component: GenericTemplate,
        redirect: to => { window.location.replace("http://www.washington.edu/anyhungryhusky/"); },
        children: [
            { path: "test-template", component: TestTemplate, name: "test-template" },
            { path: "unrecoverable", component: UnrecoverablePage, name: "unrecoverable", props: true },
        ],
    },
    { path: "*", component: NotFoundTemplate, name: "notfound" }
];
