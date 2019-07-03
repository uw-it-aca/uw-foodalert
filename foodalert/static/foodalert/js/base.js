import GenericTemplate from './components/generic-template.vue';
import LabelledInput from './components/labelled-input.vue';
import NotFoundTemplate from './components/not-found-template.vue';
import UnauthzTemplate from './components/unauthz-template.vue';
import WelcomeTemplate from './components/welcome-template.vue';
import TestTemplate from './pages/test-template.vue';
import HostWelcome from './pages/host-welcome.vue';
import StudentWelcome from './pages/student-welcome.vue';

window.vueData = {};

window.vueData.components = {
    "generic-template": GenericTemplate,
    "labelled-input": LabelledInput,
    "not-found-template": NotFoundTemplate,
    "unauthz-template": UnauthzTemplate,
    "welcome-template": WelcomeTemplate,
    "test-template": TestTemplate,
    "host-welcome": HostWelcome,
    "student-welcome": StudentWelcome,
};

window.vueData.routes = [
    {
        path: "/",
        component: GenericTemplate,
        children: [
            { path: "update", component: UnauthzTemplate, name: "update" },
            { path: "ended", component: UnauthzTemplate, name: "ended" },
            {
              path: "responsibilities",
              component: UnauthzTemplate,
              name: "responsibilities"
            },
            { path: "form", component: UnauthzTemplate, name: "form" },
            { path: "signup", component: UnauthzTemplate, name: "signup" },
            { path: "subscribed", component: UnauthzTemplate, name: "subscribed" },
            { path: "audit", component: UnauthzTemplate, name: "audit" },
            { path: "categories", component: UnauthzTemplate, name: "categories" },
            { path: "welcome", component: WelcomeTemplate, name: "welcome" },
            { path: "close", component: UnauthzTemplate, name: "close" },
            { path: "need-permit", component: UnauthzTemplate, name: "need-permit" },
            { path: "test-template", component: TestTemplate, name: "test-template" },
            { path: "food-service", component: UnauthzTemplate, name: "food-service" },
            { path: "host-welcome", component: UnauthzTemplate, name: "host-welcome" },
            { path: "student-welcome", component: UnauthzTemplate, name: "student-welcome" },
        ],
    },
    {
        path: "*",
        component: NotFoundTemplate,
        name: "notfound"
    },
];
