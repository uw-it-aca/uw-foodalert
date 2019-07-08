import FormCategory from './components/form-category.vue';
import Vue from 'vue';
import AgreePop from './components/agreement-popup.vue';
import PopContainer from './components/popup-container.vue';
import FormTemplate from './components/form-template.vue';
import FormController from './components/form-controller.vue';
import UpdateTemplate from './components/update-template.vue';
import UpdateController from './pages/update-page.vue';
import EndedTemplate from './components/ended-template.vue';
import EndedController from './pages/ended-page.vue';
import WelcomeTemplate from './components/welcome-template.vue';
import FoodCategoriesTemplate from './pages/food-categories-page.vue';
import CloseTemplate from './pages/close-page.vue';
import NeedPermit from './pages/need-permit-page.vue';
import FoodService from './pages/food-service-page.vue';
import HostWelcome from './pages/host-welcome.vue';
import ResponsibitiesPage from './pages/responsibilities-page.vue'
import FormPage from './pages/form-page.vue';

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
