import SignupTemplate from './components/signup-template.vue';
import SignupController from './components/signup-controller.vue';

Object.assign(window.vueData.components, {
    "signup-template" : SignupTemplate,
    "signup-controller" : SignupController
});

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
    { path: "signup", component: SignupController },
]);
