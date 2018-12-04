import GenericTemplate from './components/generic-template.vue';
import LabelledInput from './components/labelled-input.vue';

window.vueData = {};

window.vueData.components = {
    "generic-template": GenericTemplate,
    "labelled-input": LabelledInput,
};

window.vueData.routes = [
    {
        path: "/",
        component: GenericTemplate,
        children: [
        ],
    },
];
