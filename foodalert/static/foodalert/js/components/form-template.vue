<template>
    <b-container fluid class="p-0">
        <b-form>
            <form-category>
                <labelled-input
                    label-text="Describe the food"
                    example-text="Hot Indian buffet food"
                    :rows="2"
                    :v="v.form.description"
                    state-value="foodEvent"
                    @stateAction="this.setValue">
                </labelled-input>
                <div v-if="v.form.description.$error">
                    <p v-if="!v.form.description.required" class="hasError">Description of food is required</p>
                    <p v-if="!v.form.description.maxLength" class="hasError">The description must be shorter than 100 characters</p>
                </div>
                <labelled-input
                    label-text="Quantity"
                    example-text="About 8 full meals"
                    :rows="2"
                    :v="v.form.quantity"
                    state-value="foodQuantity"
                    @stateAction="this.setValue">
                </labelled-input>
                <div v-if="v.form.quantity.$error">
                    <p v-if="!v.form.quantity.required" class="hasError">Quantity of food is required</p>
                    <p v-if="!v.form.quantity.maxLength" class="hasError">The quantity must be shorter than 100 characters</p>
                </div>
                <labelled-input
                    label-text="End Time"
                    input-type="time"
                    example-text="6:00 PM"
                    :v="v.form.time"
                    state-value="endTime"
                    @stateAction="this.setValue">
                </labelled-input>
                <div v-if="v.form.time.$error">
                    <p v-if="!v.form.time.required" class="hasError">A designated end time is required</p>
                    <p v-if="!v.form.time.maxLength" class="hasError">The time entry must be shorter than 20 characters</p>
                </div>
                <labelled-input
                    label-text="Location"
                    example-text="e.g HUB 130"
                    :v="v.form.location"
                    state-value="location"
                    @stateAction="this.setValue">
                </labelled-input>
                <div v-if="v.form.location.$error">
                    <p v-if="!v.form.location.required" class="hasError">A designated location is required</p>
                    <p v-if="!v.form.location.maxLength" class="hasError">Description must be shorter than 40 characters</p>
                </div>
            </form-category>
            <hr>
            <form-category section-name="Food Specifications">
                <labelled-input
                    input-type="checkbox"
                    label-text="Does the food contain?"
                    :boxes='allergens'
                    state-value="allergens"
                    @stateAction="this.setValue">
                </labelled-input>




                <b-container class="bv-example-row">
                    <b-row>
                        <b-col sm >first 5</b-col>
                        <b-col sm >next 4</b-col>
                    </b-row>
                </b-container>





                <labelled-input
                    input-type="buttons"
                    label-text="Do students need to bring containers?"
                    state-value="needContainer"
                    @stateAction="this.setValue">
                </labelled-input>
            </form-category>
            <form-category section-name="Preview">
                <p v-html="previewText"></p>
            </form-category>
        </b-form>
        <hr>
        <b-container class="mb-4 d-flex justify-content-end">
            <b-link type="submit"
                    :disabled="v.form.$invalid"
                    @click="$emit('submitRequest')"
                    class="float-right btn btn-primary btn-lg py-2"> Send </b-link>
        </b-container>

        <popup-container
            :modal-show="this.modalShow"
            :mode="this.modalMode">
            <agreement-popup
                slot="default"
                intro-text="Thank you for sharing leftover food!"
                main-text="Do you have a Food Distribution Permit?"
                primary-text="Yes"
                secondary-text="No"
                :primary-action="updateValue.bind(this, 'claimsPermit')"
                :secondary-action="updateValue.bind(this, 'onSafeList')">
            </agreement-popup>
            <agreement-popup
                slot="permit"
                input-type="number"
                main-text="Enter your permit number"
                primary-text="Continue"
                can-back
                @primaryAction="this.setValue"
                state-value="permitNumber"
                :back-action="updateValue.bind(this, 'claimsPermit')">
            </agreement-popup>
            <agreement-popup
                slot="safeList"
                input-type="checkbox"
                :checkbox-options="safeFoods"
                main-text="Is your food..."
                primary-text="Continue"

                link-text="How to get a Permit"
                link-location="https://www.ehs.washington.edu/workplace/food-safety-program/temporary-food-service-permit"
                can-back
                @primaryAction="this.setValue"
                state-value="safeFoodList"
                :back-action="updateValue.bind(this, 'onSafeList')">
            </agreement-popup>
            <b-container slot="safeListConfirmation">
                <p class="text-center">You can share the foods you checked on this list </p>
                <p
                    class="text-center"
                    v-for="food in this.foodList" :key="food">
                    <strong> {{food}} </strong>
                </p>
                <p>
                    You cannot share anything that is not on that list unless you have
                    a food distribution permit.
                </p>
                <b-button
                    variant="primary"
                    class="w-100"
                    @click="updateValue('acceptedSafeListTerms')">
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
            modalShow: Boolean,
            modalMode: String,
            foodList: Array,
            v: Object,
        },
        data() {
            return {
                safeFoods: [
                    { text: "Non-perishable", value: "foodA"},
                    { text: "Commercially pre-packaged", value: "foodB"},
                    { text: "Prepared by UW Housing & Food Services", value: "foodC"},
                    { text: "None of the above", value: "foodD"},
                ],
            }
        },
        methods: {
            updateValue(context) {
                this.$emit('updateState',  context);
            },
            setValue(context, value) {
                this.$emit('setState', context, value);
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
