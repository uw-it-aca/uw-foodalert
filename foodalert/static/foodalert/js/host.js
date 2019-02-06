import FormCategory from './components/form-category.vue';
import Vue from 'vue';
import AgreePop from './components/agreement-popup.vue';
import PopContainer from './components/popup-container.vue';
import FormTemplate from './components/form-template.vue';
import FormController from './components/form-controller.vue';
import UpdateTemplate from './components/update-template.vue';
import UpdateController from './components/update-controller.vue';
import EndedTemplate from './components/ended-template.vue';
import EndedController from './components/ended-controller.vue';
import PermitCheckTemplate from './components/permit-check-template.vue'
import PermitCheckController from './components/permit-check-controller.vue'


Object.assign(window.vueData.components, {
    'form-category': FormCategory,
    'agreement-popup': AgreePop,
    'popup-container': PopContainer,
    'form-template': FormTemplate,
    'form-controller': FormController,
    'update-template': UpdateTemplate,
    'update-controller': UpdateController,
    'ended-template': EndedTemplate,
    'ended-controller': EndedController,
    'permit-check-template': PermitCheckTemplate,
    'permit-check-controller': PermitCheckController,
});

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
    { path: "update", component: UpdateController, name: "update" },
    { path: "ended", component: EndedController, name: "ended" },
    { path: "permit", component: PermitCheckController, name: "permit"},
    { path: "", component: FormController, name: "form" },
]);
