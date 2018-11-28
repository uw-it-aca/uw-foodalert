import SignupTemplate from './components/signup-template.vue';
import SignupController from './components/signup-controller.vue';

import * as main from './main.js';

main.components['signup-template'] = SignupTemplate;
main.components['signup-controller'] = SignupController;

main.routes[0].children = main.routes[0].children.concat([
    { path: "signup", component: SignupController, name: "signup" }
]);

main.router.addRoutes(main.routes);
