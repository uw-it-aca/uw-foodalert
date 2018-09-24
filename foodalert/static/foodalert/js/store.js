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
    updateFoodEvent (state, newFoodEvent) {
        state.foodEvent = newFoodEvent;
    },
    updateQuantitiy (state, newQuantity) {
        state.foodQuantity = newQuantity;
    },
    updateEndTime (state, newEndTime) {
        state.endTime = newEndTime;
    },
    updateLocation (state, newLocation) {
        state.location = newLocation;
    },
    updateAllergens (state, newAllergens) {
        state.allergens = newAllergens;
    },
    updateNeedContainer (state, needContainer) {
        state.needContainer = needContainer;
    }
}

var store = new Vuex.Store({
    state: {
        claimsPermit: false,
        permitNumber: null,
        onSafeList: false,
        safeFoodList: [],
        acceptedSafeListTerms: false,
        foodEvent: "",
        foodQuantity: "",
        endTime: "",
        location: "",
        allergens: [],
        needContainer: false,
    },
    getters: {
        previewText(state) {
            var ret = store.state.foodEvent + "<br>";
            ret += "Quantity: " + store.state.foodQuantity + "<br>";
            ret += "End Time: " + store.state.endTime + "<br>";
            ret += "Location: " + store.state.location + "<br><br>";
            ret += "May Conatain: " + store.state.allergens.join(", ") + "<br>";
            if(store.state.needContainer){
                ret += "Please bring a container";
            }
            return ret;
        }
    },
    mutations: mutations,
})

export {store, mutations};
