<template>
    <b-container fluid class="p-0">
        <b-nav v-if="navVisible" class="foodalert-sticky foodalert-navbar w-100 d-sm-none shadow-sm border-bottom py-2" fill>
            <b-nav-item href="#event" :class="{'foodalert-navbar-active': categories['Event']} "> Event </b-nav-item>
            <b-nav-item href="#food" :class="{'foodalert-navbar-active': categories['Food']} "> Food </b-nav-item>
            <b-nav-item href="#time" :class="{'foodalert-navbar-active': categories['Time']} "> Time </b-nav-item>
            <b-nav-item href="#location" :class="{'foodalert-navbar-active': categories['Location']} "> Location </b-nav-item>
        </b-nav>

        <form-category section-name="Event" icon-name="calendar" :active.sync="categories['Event']">
            <labelled-input
                label-text="What was the occasion?"
                example-text="e.g FIUTS weekly club meeting">
            </labelled-input>
        </form-category>
        <hr>
        <form-category section-name="Food" icon-name="utensils" :active.sync="categories['Food']">
            <labelled-input
                label-text="What type of food?"
                sub-label="Describe the food, cuisine, whether it's hot or cold, etc."
                example-text="e.g Hot Indian buffet food">
            </labelled-input>
            <labelled-input
                label-text="How much is left?"
                example-text="e.g. 2 large trays. About 8 full meals"
                :rows="2">
            </labelled-input>
            <labelled-input
                label-text="Do students need containers?"
                sub-label="If so, add a message here."
                example-text="e.g. Bring tupperware"
                is-optional>
            </labelled-input>
            <labelled-input
                input-type="checkbox"
                label-text="Do you know your food contains any of these allergens?"
                :boxes='allergens'
                is-optional>
            </labelled-input>
        </form-category>
        <hr>
        <form-category section-name="Time" icon-name="clock" :active.sync="categories['Time']">
            <p>Food will be available starting when you send the notification.</p>
            <labelled-input
                label-text="When will the food stop being available?"
                example-text="e.g 3:30 PM"
                warning-text="Keep in mind that food can't legally sit out unrefrigerated for more than 2 hours from the time the event starts">
            </labelled-input>
        </form-category>
        <hr>
        <form-category section-name="Location" icon-name="map-marker-alt" :active.sync="categories['Location']">
            <labelled-input
                label-text="Where will the food be located?"
                sub-label="Building name and room / room number."
                example-text="e.g HUB 130">
            </labelled-input>
            <labelled-input
                label-text="Any other details to help people find you?"
                example-text="e.g Use stairs near front desk"
                is-optional
                :rows="2">
            </labelled-input>
        </form-category>
        <hr>
        <form-category section-name="Terms and Conditions" icon-name="clipboard-check">
            <p>A brief statement about the liability that the host is taking on while posting this food, and an agreement that they have a food ditstribution permit or the food is on the "Safe to Share" list</p>
            <b-form-checkbox>
                I agree to the terms and conditions
            </b-form-checkbox>
        </form-category>
        <hr>
        <b-container class="mb-4 d-flex justify-content-end">
            <b-link href="/preview" class="float-right btn btn-primary btn-lg py-2"> Preview Notification </b-link>
        </b-container>

        <popup-container
            :modal-show="$store.getters.modalShow"
            :mode="$store.getters.modalMode">
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
        },
        computed: {
            navVisible: function () {
                var ret = false;
                for (var cat in this.categories) {
                    ret = ret || this.categories[cat];
                }
                return ret;
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
                categories: {
                    Event: false,
                    Food: false,
                    Time: false,
                    Location: false,
                },
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
