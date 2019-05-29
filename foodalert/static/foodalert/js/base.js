import GenericTemplate from './components/generic-template.vue';
import LabelledInput from './components/labelled-input.vue';
import NotFoundTemplate from './components/not-found-template.vue';
import UnauthzTemplate from './components/unauthz-template.vue';
import WelcomeTemplate from './components/welcome-template.vue';

window.vueData = {};

window.vueData.components = {
    "generic-template": GenericTemplate,
    "labelled-input": LabelledInput,
    "not-found-template": NotFoundTemplate,
    "unauthz-template": UnauthzTemplate,
    "welcome-template": WelcomeTemplate,
};

window.vueData.routes = [
  { path: "/welcome", component: UnauthzTemplate},

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
            { path: "", component: UnauthzTemplate, name: "form" },
            { path: "signup", component: UnauthzTemplate },
            { path: "subscribed", component: UnauthzTemplate },
            { path: "audit", component: UnauthzTemplate },
            { path: "welcome", component: WelcomeTemplate },
        ],
    },
    {
        path: "*",
        component: NotFoundTemplate,
    },
];
