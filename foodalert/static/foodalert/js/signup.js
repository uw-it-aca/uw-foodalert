import StudentWelcome from './pages/student/welcome.vue';
import ResponsibitiesPage from './pages/student/responsibilities-page.vue';
import NotificationPage from './pages/student/notification-page.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
    //{ path: "signup", component: SignupController },
    //{ path: "subscribed", component: SubscribedController },
    { path: "student-welcome", component: StudentWelcome },
]);

let rootPath = window.vueData.routes.find(obj => obj.path === "/s/");
function activatePage(name, page, title) {
    let route = rootPath.children.find(obj => obj.path === name)
    route.component = page
    route.meta.title = title
}

activatePage("welcome", StudentWelcome, "Find surplus food on campus")
activatePage("responsibilities", ResponsibitiesPage, "Terms of service")
activatePage("notifications", NotificationPage, "Choose how you want to be notified")
