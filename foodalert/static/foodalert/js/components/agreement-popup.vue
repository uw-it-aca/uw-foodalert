<template>
    <div class="px-4">
        <a v-if="canBack" class="ml-0 mb-4" @click="backAction"> Back </a>
        <p v-if="canBack"><br></p>
        <p v-if="introText" class="h5 text-center mt-4 mb-5 text-center font-weight-light"> &nbsp; {{ introText }}</p>
        <p class="h5 text-center mb-3"> {{ mainText }} </p>
        <b-form-group>
            <b-form-input
                v-if="inputType == 'number'"
                v-model="value"
                type="number"
                placeholder="40569503"
                class="text-center mb-3 border-0">
            </b-form-input>
            <b-form-checkbox-group
                v-if="inputType == 'checkbox'"
                v-model="value"
                stacked
                class="ml-5"
                :options="checkboxOptions">
            </b-form-checkbox-group>
        </b-form-group>
        <div v-if="primaryText || secondaryText" class="d-flex justify-content-center">
            <b-button
                v-if="secondaryText"
                class="px-5"
                size="lg"
                variant="secondary"
                @click="secondaryAction">
                {{ secondaryText }}
            </b-button>
            <b-button
                v-if="primaryText"
                :class="['px-5', {'ml-2': secondaryText}]"
                size="lg"
                variant="primary"
                @click="primarySubmit">
                {{ primaryText }}
            </b-button>
        </div>
        <br>
        <p v-if="infoText" class="d-block text-center w-100 text-center mt-4 mb-3 font-italic"> {{ infoText }} </p>
        <a v-if="linkText" :href="linkLocation" class="d-block text-center mb-3"> {{ linkText }} </a>
    </div>
</template>


<script>
    export default {
        props: {
            inputType: {
                type: String,
                required: false,
                validator: function (value) {
                    return [
                        'number',
                        'checkbox',
                    ].indexOf(value) !== -1;
                }
            },
            checkboxOptions: Array,
            mainText: String,
            introText: String,
            infoText: String,
            linkText: String,
            linkLocation: String,
            primaryText: String,
            secondaryText: String,
            canBack: Boolean,
            primaryAction: Function,
            secondaryAction: Function,
            backAction: Function,
            stateValue: String,
        },
        data() {
            return {
                value: null,
            }
        },
        methods: {
            primarySubmit: function () {
                if (this.primaryAction) {
                    return this.primaryAction();
                } else {
                    return this.$emit('primaryAction', this.stateValue, this.value);
                }
            },
        },
        mounted() {
            if (this.inputType == 'checkbox') {
                this.value = [];
            }
        },
    }
</script>

<style>

</style>
