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
function activatePage(name, page, title) {
    let route = rootPath.children.find(obj => obj.path === name)
    route.component = page
    route.meta.title = title
}

activatePage("update", UpdateController, "Send out food service updates")
activatePage("ended", EndedController, "Thank you for sharing food")
activatePage("welcome", HostWelcome, "Share your leftover event food - Hungry Husky")
activatePage("categories", FoodCategoriesTemplate, "Share more about your food with us")
activatePage("form", FormPage, "Make a notification to share food")
activatePage("close", CloseTemplate, "You won't be able to share food with us")
activatePage("need-permit", NeedPermit, "You won't be able to share food with us at this time")
activatePage("food-service", FoodService, "Help us determine if your food is shareable")
activatePage("responsibilities", ResponsibitiesPage, "We need you to agree to a few things")
