import FormCategory from './components/form-category.vue';
import Vue from 'vue';
import AgreePop from './components/agreement-popup.vue';
import PopContainer from './components/popup-container.vue';
import FormTemplate from './components/form-template.vue';
import FormController from './components/form-controller.vue';
import UpdateTemplate from './components/update-template.vue';
import UpdateController from './components/update-controller.vue';
import EndedTemplate from './components/ended-template.vue';
import EndedController from './components/ended-controller.vue';
import WelcomeTemplate from './components/welcome-template.vue';
import FoodCategoriesTemplate from './components/food-categories-template.vue';
import CloseTemplate from './components/close-template.vue';
import NeedPermit from './components/need-permit-template.vue';

Object.assign(window.vueData.components, {
    'form-category': FormCategory,
    'agreement-popup': AgreePop,
    'popup-container': PopContainer,
    'form-template': FormTemplate,
    'form-controller': FormController,
    'update-template': UpdateTemplate,
    'update-controller': UpdateController,
    'ended-template': EndedTemplate,
    'ended-controller': EndedController,
    'welcome-template': WelcomeTemplate,
    'food-categories-template': FoodCategoriesTemplate,
    'close-template': CloseTemplate,
    'need-permit': NeedPermit,
});

let rootPath = window.vueData.routes.find(obj => obj.path === "/");
rootPath.children.find(obj => obj.path === "update").component = UpdateController;
rootPath.children.find(obj => obj.path === "ended").component = EndedController;
rootPath.children.find(obj => obj.path === "welcome").component = WelcomeTemplate;
rootPath.children.find(obj => obj.path === "categories").component = FoodCategoriesTemplate;
rootPath.children.find(obj => obj.path === "").component = FormController;
rootPath.children.find(obj => obj.path === "close").component = CloseTemplate;
rootPath.children.find(obj => obj.path === "need-permit").component = NeedPermit;
