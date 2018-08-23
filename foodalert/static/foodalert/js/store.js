import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);

var store = new Vuex.Store({
    state: {
        claimsPermit: false,
        permitNumber: null,
        onSafeList: false,
        safeFoodList: [],
    },
    getters: {
        modalShow(state) {
            //show the model so long as one of the field sets is incomplete
            return (!state.claimsPermit || !state.permitNumber) &&
                   (!state.onSafeList || state.safeFoodList.length == 0);
        },
        modalMode (state) {
            if (state.claimsPermit) {
                return "permit";
            }
            if (state.onSafeList) {
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
    }
})

export {store};
