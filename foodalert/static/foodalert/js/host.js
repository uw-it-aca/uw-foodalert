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

import * as main from './main.js';

Vue.component('ended-controller', EndedController);

//Object.assign(main.components, {
//    'form-category': FormCategory,
//    'agreement-popup': AgreePop,
//    'popup-container': PopContainer,
//    'form-template': FormTemplate,
//    'form-controller': FormController,
//    'update-template': UpdateTemplate,
//    'update-controller': UpdateController,
//    'ended-template': EndedTemplate,
//    'ended-controller': EndedController,
//});

main.routes[0].children = main.routes[0].children.concat([
    { path: "update", component: UpdateController, name: "update" },
    { path: "ended", component: EndedController, name: "ended", beforeEnter: (to,from,next) => {
        console.log("navigating to ended");
        next();
    }},
    { path: "", component: FormController, name: "form", beforeEnter: (to,from,next) => {
        console.log("navigating to form");
        next();
   }},
]);

console.log(main.app);
//main.routes.push({path:"/test", component:EndedTemplate, name:"test"});
//main.app.$router.push("test");
main.app.$router.addRoutes(main.routes);
//console.log(main.app.$router);
//console.log("");
//main.app.$router.push("loading");
//main.app.$router.push({path:"/ended"});
//main.app.$router.push({path:"/"});
