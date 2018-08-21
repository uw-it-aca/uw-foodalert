import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);

var store = new Vuex.Store({
    state: {
        navVisible: true,
        currentCat: "",
        scrollY: window.scrollY,
    },
    mutations: {
        showNav (state) {
            state.navVisible = true;
        },
        hideNav (state) {
            state.navVisible = false;
        },
        setCurrentCat (state, id) {
            state.currentCat = id;
        },
    }
})

export {store};
