<template>
    <b-container class="px-0">
        <b-container>
            <p>You are signing up to be notified about leftover food after on-campus events.</p>
            <a href="#"> Learn More </a>
        </b-container>
        <hr>
        <form-category
            section-name="Notification Method">
            <b-form-checkbox-group
                :options="['Email','SMS/Text']"
                stacked
                :checked="inputTypes"
                @input="$emit('update:inputTypes', $event)"
                class="mb-3">
            </b-form-checkbox-group>
            <labelled-input
                label-text="Email"
                input-type="textarea"
                :v="v.val.email"
                v-if="inputTypes.indexOf('Email') !== -1"
                @input="this.$emit('update:email', $event)"
                no-padding
                no-char-count>
            </labelled-input>
            <div v-if="v.val.email.$error">
                <p v-if="!v.val.email.emailIf" class="hasError">Email must be in correct email format (e.g. abc@xyz.com)</p>
                <p v-if="!v.val.email.requiredIf" class="hasError">Please provide an email or unselect the email checkbox</p>
            </div>
            <labelled-input
                label-text="SMS/Text Number"
                input-type="textarea"
                :v="v.val.sms"
                v-if="inputTypes.indexOf('SMS/Text') !== -1"
                @input="this.$emit('update:sms', $event)"
                no-padding
                no-char-count>
            </labelled-input>
            <div v-if="v.val.sms.$error">
                <p v-if="!v.val.sms.requiredIf" class="hasError">Please provide a number or unselect the sms checkbox</p>
                <p v-if="!v.val.sms.phoneNumIf" class="hasError">Number must be in correct number format (e.g. 123-123-1234)</p>
            </div>
        </form-category>
        <hr>
        <form-category
            section-name="Terms of Agreement">
            <p>
                <strong> Food Safety </strong>
                <br>
                This is some text talking about food safety. We're not 100% sure what it will say, but it will be kinda long.
            </p>
            <p>
                <strong> Allergens </strong>
                <br>
                This is some text talking about allergens. We're not 100% sure what it will say, but it will be kinda long.
            </p>
            <b-form-checkbox
                @input="$emit('update:agreement', $event)">
                I agree to the terms and conditions.
            </b-form-checkbox>
        </form-category>
        <hr>
        <b-container>
            <b-link
                :disabled="v.val.$invalid || this.inputTypes.length === 0 || !this.agreement"
                class="btn btn-primary float-right mb-3"
                @click="$emit('send')">
                Sign Up
            </b-link>
        </b-container>
    </b-container>
</template>

<script>
    import FormCategory from './form-category.vue';
    import LabelledInput from './labelled-input.vue';
    import { parsePhoneNumberFromString } from 'libphonenumber-js'

    export default {
        props: {
            v: Object,
            inputTypes: Array,
            email: String,
            sms: String,
            agreement: Boolean,
        },
        data() {
            return {}
        },
        components: {
            'form-category': FormCategory,
            'labelled-input': LabelledInput,
        },
    }
</script>
