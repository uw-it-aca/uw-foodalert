<template>
    <b-container fluid class="p-0">
        <b-form>
            <form-category>
                <labelled-input
                    label-text="Event Name"
                    example-text="FIUTS weekly club meeting"
                    :rows="1"
                    :v="v.form.event"
                    state-value="event"
                    @stateAction="this.setValue">
                </labelled-input>
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
            <form-category section-name="Food Specifications">
                <labelled-input
                    input-type="checkbox"
                    label-text="Does the food contain?"
                    :boxes='allergens'
                    state-value="allergens"
                    @stateAction="this.setValue">
                </labelled-input>
                <labelled-input
                    input-type="buttons"
                    label-text="Do students need to bring containers?"
                    state-value="needContainer"
                    @stateAction="this.setValue">
                </labelled-input>
            </form-category>
            <form-category section-name="Message Preview">
                <p style="color: green">{{previewText.heading}}</p>
                <p>{{previewText.food}}</p>
                <p>{{previewText.location}}</p>
                <p>{{previewText.quantity}}</p>
                <p>{{previewText.time}}</p>
                <p>{{previewText.allergens}}</p>
                <p>{{previewText.container}}</p>
                <br>
            </form-category>
        </b-form>
        <b-container class="mb-4 d-flex justify-content-end">
            <b-link type="submit"
                    :disabled="v.form.$invalid"
                    @click="showModal"
                    class="float-right btn btn-primary btn-lg py-2"> Send </b-link>
        </b-container>

        <b-modal
            v-model="modalShow"
            title="Confirmation"
            title-tag="h3"
            header-border-variant="light"
            footer-border-variant="light"
            header-bg-variant="light"
            footer-bg-variant="light"
            body-bg-variant="light"
            :hide-header-close="true"
            ok-title="Send"
            @ok="$emit('submitRequest')">
            We will send your notification to Hungry Husky Subscribers.
        </b-modal>

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
            previewText: Object,
            modalMode: String,
            foodList: Array,
            v: Object,
        },
        data() {
            return {
                modalShow: false,
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
            showModal() {
                this.modalShow = true;
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
