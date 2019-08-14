import {activatePage} from './utils.js';
import UpdateController from './pages/host/update-page.vue';
import EndedController from './pages/host/ended-page.vue';
import FoodCategoriesTemplate from './pages/host/food-categories-page.vue';
import CloseTemplate from './pages/host/close-page.vue';
import NeedPermit from './pages/host/need-permit-page.vue';
import FoodService from './pages/host/food-service-page.vue';
import HostWelcome from './pages/host/welcome.vue';
import ResponsibitiesPage from './pages/host/responsibilities-page.vue';
import FormPage from './pages/host/form-page.vue';

const rootPath = window.vueData.routes.find((obj) => obj.path === '/h/');

activatePage(rootPath, 'update', UpdateController,
    'Send out food service updates');
activatePage(rootPath, 'ended', EndedController, 'Thank you for sharing food');
activatePage(rootPath, 'welcome', HostWelcome,
    'Share your leftover event food - Hungry Husky');
activatePage(rootPath, 'categories', FoodCategoriesTemplate,
    'Share more about your food with us');
activatePage(rootPath, 'form', FormPage, 'Make a notification to share food');
activatePage(rootPath, 'close', CloseTemplate,
    'You won\'t be able to share food with us');
activatePage(rootPath, 'need-permit', NeedPermit,
    'You won\'t be able to share food with us at this time');
activatePage(rootPath, 'food-service', FoodService,
    'Help us determine if your food is shareable');
activatePage(rootPath, 'responsibilities', ResponsibitiesPage,
    'We need you to agree to a few things');
