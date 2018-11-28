import FormCategory from './components/form-category.vue';
import AgreePop from './components/agreement-popup.vue';
import PopContainer from './components/popup-container.vue';
import FormTemplate from './components/form-template.vue';
import FormController from './components/form-controller.vue';
import UpdateTemplate from './components/update-template.vue';
import UpdateController from './components/update-controller.vue';
import EndedTemplate from './components/ended-template.vue';
import EndedController from './components/ended-controller.vue';

import * as main from './main.js';

Object.assign(main.components, {
    'form-category': FormCategory,
    'agreement-popup': AgreePop,
    'popup-container': PopContainer,
    'form-template': FormTemplate,
    'form-controller': FormController,
    'update-template': UpdateTemplate,
    'update-controller': UpdateController,
    'ended-template': EndedTemplate,
    'ended-controller': EndedController,
});

main.routes[1].children = main.routes[1].children.concat([
    { path: "update", component: UpdateController, name: "update" },
    { path: "ended", component: EndedController, name: "ended" },
    { path: "", component: FormController, name: "form" },
]);

main.app.$router.addRoutes(main.routes);
main.app.$router.push("loading");
main.app.$router.push({path:"/"});
