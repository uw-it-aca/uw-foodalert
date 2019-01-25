import GenericTemplate from './components/generic-template.vue';
import LabelledInput from './components/labelled-input.vue';
import NotFoundTemplate from './components/not-found-template.vue';

window.vueData = {};

window.vueData.components = {
    "generic-template": GenericTemplate,
    "labelled-input": LabelledInput,
    "not-found-template": NotFoundTemplate,
};

window.vueData.routes = [
    {
        path: "/",
        component: GenericTemplate,
        children: [
        ],
    },
    {
        path: "*",
        component: NotFoundTemplate,
    },
];
