import SignupTemplate from './components/signup-template.vue';
import SignupController from './components/signup-controller.vue';
import SubscribedTemplate from './components/subscribed-template.vue';
import SubscribedController from './components/subscribed-controller.vue';
import StudentWelcome from './pages/student/welcome.vue';
import ResponsibitiesPage from './pages/student/responsibilities-page.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
    { path: "signup", component: SignupController },
    { path: "subscribed", component: SubscribedController },
    { path: "student-welcome", component: StudentWelcome },
]);

let rootPath = window.vueData.routes.find(obj => obj.path === "/");
rootPath.children.find(obj => obj.path === "s/signup").component = SignupController;
rootPath.children.find(obj => obj.path === "s/subscribed").component = SubscribedController;
rootPath.children.find(obj => obj.path === "s/welcome").component = StudentWelcome;
rootPath.children.find(obj => obj.path === "s/responsibilities").component = ResponsibitiesPage;
