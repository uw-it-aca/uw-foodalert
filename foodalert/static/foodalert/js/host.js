import UpdateController from './pages/host/update-page.vue';
import EndedController from './pages/host/ended-page.vue';
import FoodCategoriesTemplate from './pages/host/food-categories-page.vue';
import CloseTemplate from './pages/host/close-page.vue';
import NeedPermit from './pages/host/need-permit-page.vue';
import FoodService from './pages/host/food-service-page.vue';
import HostWelcome from './pages/host/welcome.vue';
import ResponsibitiesPage from './pages/host/responsibilities-page.vue'
import FormPage from './pages/host/form-page.vue';

let rootPath = window.vueData.routes.find(obj => obj.path === "/");
rootPath.children.find(obj => obj.path === "h/update").component = UpdateController;
rootPath.children.find(obj => obj.path === "h/ended").component = EndedController;
rootPath.children.find(obj => obj.path === "h/welcome").component = HostWelcome;
rootPath.children.find(obj => obj.path === "h/categories").component = FoodCategoriesTemplate;
rootPath.children.find(obj => obj.path === "h/form").component = FormPage;
rootPath.children.find(obj => obj.path === "h/close").component = CloseTemplate;
rootPath.children.find(obj => obj.path === "h/need-permit").component = NeedPermit;
rootPath.children.find(obj => obj.path === "h/food-service").component = FoodService;
rootPath.children.find(obj => obj.path === "h/responsibilities").component = ResponsibitiesPage;
