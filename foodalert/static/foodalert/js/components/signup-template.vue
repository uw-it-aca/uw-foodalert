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
                :value="inputTypes"
                @input="setValue($event)"
                class="mb-3">
            </b-form-checkbox-group>
            <labelled-input
                label-text="Email"
                input-type="textarea"
                :v="v.form.email"
                v-if="inputTypes.indexOf('Email') !== -1"
                no-padding
                no-char-count>
            </labelled-input>
            <div v-if="v.form.email.$error">
                <p v-if="!v.form.email.email" class="hasError">Email must be in correct email format (e.g. abc@xyz.com)</p>
                <p v-if="!v.form.email.required" class="hasError">Please provide an email or unselect the email checkbox</p>
            </div>
            <labelled-input
                label-text="SMS/Text Number"
                input-type="textarea"
                :v="v.form.sms"
                v-if="inputTypes.indexOf('SMS/Text') !== -1"
                no-padding
                no-char-count>
            </labelled-input>
            <div v-if="v.form.sms.$error">
                <p v-if="!v.form.sms.required" class="hasError">Please provide a number or unselect the sms checkbox</p>
                <p v-if="!v.form.sms.phoneNum" class="hasError">Number must be in correct number format (e.g. 123-123-1234)</p>
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
                v-model="agreement">
                I agree to the terms and conditions.
            </b-form-checkbox>
        </form-category>
        <hr>
        <b-container>
            <b-link
                :disabled="v.form.$invalid || this.inputTypes.length === 0 || !this.agreement"
                class="btn btn-primary float-right mb-3"
                href="/subscribed">
                Sign Up
            </b-link>
        </b-container>
    </b-container>
</template>

<script>
    import FormCategory from './form-category.vue';
    import LabelledInput from './labelled-input.vue';

    export default {
        props: {
            v: Object,
        },
        data() {
            return {
                inputTypes: [],
                agreement: false,
            }
        },
        components: {
            'form-category': FormCategory,
            'labelled-input': LabelledInput,
        },
        methods: {
            setValue(payload) {
                this.inputTypes = payload;
                this.$emit('updateInput', payload);
            },
        },
    }
</script>
