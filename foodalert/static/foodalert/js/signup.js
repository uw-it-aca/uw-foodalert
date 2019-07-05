import SignupTemplate from './components/signup-template.vue';
import SignupController from './components/signup-controller.vue';
import SubscribedTemplate from './components/subscribed-template.vue';
import SubscribedController from './components/subscribed-controller.vue';
import StudentWelcome from './pages/student-welcome.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
    { path: "signup", component: SignupController },
    { path: "subscribed", component: SubscribedController },
    { path: "student-welcome", component: StudentWelcome },
]);

let rootPath = window.vueData.routes.find(obj => obj.path === "/");
rootPath.children.find(obj => obj.path === "signup").component = SignupController;
rootPath.children.find(obj => obj.path === "subscribed").component = SubscribedController;
rootPath.children.find(obj => obj.path === "student-welcome").component = StudentWelcome;
