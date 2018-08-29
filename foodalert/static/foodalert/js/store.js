import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);

var mutations = {
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
    rejectSafeListTerms (state) {
        state.acceptedSafeListTerms = false;
    },
}

var store = new Vuex.Store({
    state: {
        claimsPermit: false,
        permitNumber: null,
        onSafeList: false,
        safeFoodList: [],
        acceptedSafeListTerms: false,
    },
    mutations: mutations,
})

export {store, mutations};
