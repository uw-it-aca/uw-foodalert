
import {activatePage} from './utils.js';
import StudentWelcome from './pages/student/welcome.vue';
import ResponsibitiesPage from './pages/student/responsibilities-page.vue';
import NotificationPage from './pages/student/notification-page.vue';

window.vueData.routes[0].children = window.vueData.routes[0].children.concat([
  {path: 'student-welcome', component: StudentWelcome},
]);

const rootPath = window.vueData.routes.find((obj) => obj.path === '/s/');

activatePage(rootPath, 'welcome', StudentWelcome,
    'Find surplus food on campus');
activatePage(rootPath, 'responsibilities', ResponsibitiesPage,
    'Terms of service');
activatePage(rootPath, 'notifications', NotificationPage,
    'Choose how you want to be notified');
