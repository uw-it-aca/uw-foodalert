import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);

var store = new Vuex.Store({
    state: {
        navVisible: true,
        currentCat: "",
        claimsPermit: false,
        permitNumber: null,
        onSafeList: false,
        safeFoodList: [],
        acceptedSafeListTerms: false,
    },
    getters: {
        modalShow(state) {
            //show the model so long as one of the field sets is incomplete
            return (!state.claimsPermit || !state.permitNumber) &&
                   (!state.onSafeList || state.safeFoodList.length == 0 || !state.acceptedSafeListTerms);
        },
        modalMode (state) {
            if (state.claimsPermit) {
                return "permit";
            }
            if (state.onSafeList) {
                if (state.safeFoodList.length) {
                    return "safeListConfirmation";
                }
                return "safeList";
            }
            return "default";
        }
    },
    mutations: {
        claimPermit (state) {
            state.claimsPermit = true;
        },
        relinquishPermit (state) {
            state.claimsPermit = false;
        },
        setPermitNumber (state, permitNumber) {
            state.permitNumber = permitNumber;
        },
        claimSafeFood (state) {
            state.onSafeList = true;
        },
        relinquishSafeFood (state) {
            state.onSafeList = false;
        },
        setSafeFoods (state, foods) {
            state.safeFoodList = foods;
        },
        acceptSafeListTerms (state) {
            state.acceptedSafeListTerms = true;
        },
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
