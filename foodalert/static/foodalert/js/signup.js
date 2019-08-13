import StudentWelcome from './pages/student/welcome.vue';
import ResponsibitiesPage from './pages/student/responsibilities-page.vue';
import NotificationPage from './pages/student/notification-page.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
    //{ path: "signup", component: SignupController },
    //{ path: "subscribed", component: SubscribedController },
    { path: "student-welcome", component: StudentWelcome },
]);

let rootPath = window.vueData.routes.find(obj => obj.path === "/s/");
rootPath.children.find(obj => obj.path === "welcome").component = StudentWelcome;
rootPath.children.find(obj => obj.path === "responsibilities").component = ResponsibitiesPage;
rootPath.children.find(obj => obj.path === "notifications").component = NotificationPage;
