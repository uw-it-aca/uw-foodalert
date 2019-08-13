import UpdateController from './pages/host/update-page.vue';
import EndedController from './pages/host/ended-page.vue';
import FoodCategoriesTemplate from './pages/host/food-categories-page.vue';
import CloseTemplate from './pages/host/close-page.vue';
import NeedPermit from './pages/host/need-permit-page.vue';
import FoodService from './pages/host/food-service-page.vue';
import HostWelcome from './pages/host/welcome.vue';
import ResponsibitiesPage from './pages/host/responsibilities-page.vue'
import FormPage from './pages/host/form-page.vue';

let rootPath = window.vueData.routes.find(obj => obj.path === "/h/");
rootPath.children.find(obj => obj.path === "update").component = UpdateController;
rootPath.children.find(obj => obj.path === "ended").component = EndedController;
rootPath.children.find(obj => obj.path === "welcome").component = HostWelcome;
rootPath.children.find(obj => obj.path === "categories").component = FoodCategoriesTemplate;
rootPath.children.find(obj => obj.path === "form").component = FormPage;
rootPath.children.find(obj => obj.path === "close").component = CloseTemplate;
rootPath.children.find(obj => obj.path === "need-permit").component = NeedPermit;
rootPath.children.find(obj => obj.path === "food-service").component = FoodService;
rootPath.children.find(obj => obj.path === "responsibilities").component = ResponsibitiesPage;
