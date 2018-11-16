<template>
    <b-container fluid class="p-0">
        <b-form>
            <form-category>
                <labelled-input
                    label-text="Describe the food and event"
                    example-text="hot indian food FIUTS weekly club meeting"
                    :rows="2"
                    v-model.trim="form.description"
                    :v="$v.form.description"
                    store-commit="updateFoodEvent">
                </labelled-input>
                <div v-if="$v.form.description.$error">
                    <p v-if="!$v.form.description.required" class="hasError">Description of food is required</p>
                    <p v-if="!$v.form.description.maxLength" class="hasError">The description must be shorter than 100 characters</p>
                </div>
                <labelled-input
                    label-text="Quantity"
                    example-text="About 8 full meals"
                    :rows="2"
                    v-model.trim="form.quantity"
                    :v="$v.form.quantity"
                    store-commit="updateQuantitiy">
                </labelled-input>
                <div v-if="$v.form.quantity.$error">
                    <p v-if="!$v.form.quantity.required" class="hasError">Quantity of food is required</p>
                    <p v-if="!$v.form.quantity.maxLength" class="hasError">The quantity must be shorter than 100 characters</p>
                </div>
                <labelled-input
                    label-text="End Time"
                    input-type="time"
                    example-text="6:00 PM"
                    v-model.trim="form.time"
                    :v="$v.form.time"
                    store-commit="updateEndTime">
                </labelled-input>
                <div v-if="$v.form.time.$error">
                    <p v-if="!$v.form.time.required" class="hasError">A designated end time is required</p>
                    <p v-if="!$v.form.time.maxLength" class="hasError">The time entry must be shorter than 20 characters</p>
                </div>
                <labelled-input
                    label-text="Location"
                    example-text="e.g HUB 130"
                    v-model.trim="form.location"
                    :v="$v.form.location"
                    store-commit="updateLocation">
                </labelled-input>
                <div v-if="$v.form.location.$error">
                    <p v-if="!$v.form.location.required" class="hasError">A designated location is required</p>
                    <p v-if="!$v.form.location.maxLength" class="hasError">Description must be shorter than 40 characters</p>
                </div>
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
        </b-form>
        <hr>
        <b-container class="mb-4 d-flex justify-content-end">
            <b-link type="submit"
                    to="update"
                    :disabled="$v.form.$invalid"
                    @click="buildRequest"
                    class="float-right btn btn-primary btn-lg py-2"> Send Notification </b-link>
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
    import Cookies from 'js-cookie';
    import { validationMixin } from "vuelidate"
    import { required, maxLength } from "vuelidate/lib/validators"
    const axios = require('axios');
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
                form : {
                    description: "",
                    quantity: "",
                    time: "",
                    location: ""
                }
            }
        },
        validations: {
            form: {
                description: {
                    required,
                    maxLength: maxLength(100)
                },
                quantity: {
                    required,
                    maxLength: maxLength(100)
                },
                time: {
                    required,
                    maxLength: maxLength(20)
                },
                location: {
                    required,
                    maxLength: maxLength(40)
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
            buildRequest() {
                var data = {
                     "location": {
                          "main": this.$store.state.location.substring(0, 10),
                          "detail": this.$store.state.location
                     },
                     "event": "Placeholder event",
                     "time": {
                         "created": new Date(),
                         "ended": new Date((new Date()).toString().substring(0,16) + this.$store.state.endTime + ":00")
                     },
                     "food": {
                         "served": this.$store.state.foodEvent,
                         "amount": this.$store.state.foodQuantity,
                         "allergens": this.$store.state.allergens
                     },
                     "bringContainers": this.$store.state.needContainer,
                     "foodServiceInfo": {
                         "permitNumber": this.$store.state.permitNumber,
                         "safeToShareFood": this.$store.state.safeFoodList
                     },
                     "host": {
                         "hostID": 1,
                         "userAgent": navigator.userAgent
                     }
                };
                var csrftoken = Cookies.get('csrftoken');
                var headers = {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                }
                axios.post('/notification/', data, {"headers": headers})
                    .then(function (response) {
                        console.log(response);
                    })
                    .catch(function (error) {
                        alert("There was an error processing the request");
                        console.log(error);
                    })
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
