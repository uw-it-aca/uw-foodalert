<template>
    <b-container fluid class="p-0">
        <form-category>
            <labelled-input
                label-text="Describe the food and event"
                example-text="hot indian food FIUTS weekly club meeting"
                :rows="2"
                store-commit="updateFoodEvent">
            </labelled-input>
            <labelled-input
                label-text="Quantity"
                example-text="About 8 full meals"
                :rows="2"
                store-commit="updateQuantitiy">
            </labelled-input>
            <labelled-input
                label-text="End Time"
                input-type="time"
                example-text="6:00 PM"
                store-commit="updateEndTime">
            </labelled-input>
            <labelled-input
                label-text="Location"
                example-text="e.g HUB 130"
                store-commit="updateLocation">
            </labelled-input>
        </form-category>
        <hr>
        <form-category section-name="Food Specifications">
            <labelled-input
                input-type="checkbox"
                label-text="Does the food contain?"
                :boxes='allergens'
                store-commit="updateAllergens">
            </labelled-input>
            <labelled-input
                input-type="buttons"
                label-text="Do students need to bring containers?"
                store-commit="updateNeedContainer">
            </labelled-input>
        </form-category>
        <form-category section-name="Preview">
            <p v-html="previewText"></p>
        </form-category>
        <hr>
        <b-container class="mb-4 d-flex justify-content-end">
            <b-link href="/preview" class="float-right btn btn-primary btn-lg py-2"> Preview Notification </b-link>
        </b-container>

        <popup-container
            :modal-show="modalShow"
            :mode="modalMode">
            <agreement-popup
                slot="default"
                intro-text="Thank you for sharing leftover food!"
                main-text="Do you have a Food Distribution Permit?"
                primary-text="Yes"
                secondary-text="No"
                :primary-action="$store.commit.bind(this, 'claimPermit')"
                :secondary-action="$store.commit.bind(this, 'claimSafeFood')">
            </agreement-popup>
            <agreement-popup
                slot="permit"
                input-type="number"
                primary-store-mutation="setPermitNumber"
                main-text="Enter your permit number"
                primary-text="Continue"
                can-back
                :back-action="$store.commit.bind(this, 'relinquishPermit')">
            </agreement-popup>
            <agreement-popup
                slot="safeList"
                input-type="checkbox"
                :checkbox-options="safeFoods"
                primary-store-mutation="setSafeFoods"
                main-text="Is the food you are sharing listed below?"
                primary-text="Continue"
                info-text="If your food is NOT on this list, you need a permit to share it"
                link-text="How to get a Permit"
                link-location="https://www.ehs.washington.edu/workplace/food-safety-program/temporary-food-service-permit"
                can-back
                :back-action="$store.commit.bind(this, 'relinquishSafeFood')">
            </agreement-popup>
            <b-container
                slot="safeListConfirmation">
                <p class="text-center">You can share the foods you checked on this list </p>
                <p
                    class="text-center"
                    v-for="food in $store.state.safeFoodList">
                    <strong> {{food}} </strong>
                </p>
                <p>
                    You cannot share anything that is not on that list unless you have
                    a food distribution permit.
                </p>
                <b-button
                    variant="primary"
                    class="w-100"
                    @click="$store.commit('acceptSafeListTerms')">
                    I Understand
                </b-button>
            </b-container>
        </popup-container>
    </b-container>
</template>

<script>
    import FormCategory from './form-category.vue';
    import LabelledInput from './labelled-input.vue';
    import PopupContainer from './popup-container.vue';
    import AgreePop from './agreement-popup.vue';
    export default {
        props: {
            allergens: Array,
            previewText: String,
        },
        computed: {
            navVisible: function () {
                var ret = false;
                for (var cat in this.categories) {
                    ret = ret || this.categories[cat];
                }
                return ret;
            },
            modalShow: function() {
                //show the model so long as one of the field sets is incomplete
                return (
                    (!this.$store.state.claimsPermit || !this.$store.state.permitNumber) &&
                    (
                        !this.$store.state.onSafeList ||
                        this.$store.state.safeFoodList.length == 0 ||
                        !this.$store.state.acceptedSafeListTerms
                    )
                );
            },
            modalMode: function() {
                if (this.$store.state.claimsPermit) {
                    return "permit";
                }
                if (this.$store.state.onSafeList) {
                    if (this.$store.state.safeFoodList.length) {
                        return "safeListConfirmation";
                    }
                    return "safeList";
                }
                return "default";
            }
        },
        data() {
            return {
                safeFoods: [
                    { text: "Food A", value: "foodA"},
                    { text: "Food B", value: "foodB"},
                    { text: "Food C", value: "foodC"},
                    { text: "Food D", value: "foodD"},
                ],
            }
        },
        methods: {
            claimPermit() {
                this.$store.commit('claimPermit');
            },
            relinquishPermit() {
                this.$store.commit('relinquishPermit');
            },
            claimSafeFood() {
                this.$store.commit('claimSafeFood');
            },
            relinquishSafeFood() {
                this.$store.commit('relinquishSafeFood');
            },
        },
        components: {
            'form-category': FormCategory,
            'labelled-input': LabelledInput,
            'popup-container': PopupContainer,
            'agreement-popup': AgreePop,
        }
    }
</script>
