<template>
    <b-container class="px-0">
        <b-container>
            <p>You are signing up to be notified about leftover food after on-campus events.</p>
            <a href="#"> Learn More </a>
        </b-container>
        <hr>
        <form-category
            section-name="Notification Method"
            icon-name="bell">
            <b-form-checkbox-group
                :options="['Email','SMS/Text']"
                stacked
                v-model="inputTypes"
                class="mb-3">
            </b-form-checkbox-group>
            <labelled-input
                label-text="Email"
                input-type="textarea"
                v-if="inputTypes.indexOf('Email') !== -1"
                no-padding
                no-char-count>
            </labelled-input>
            <labelled-input
                label-text="SMS/Text Number"
                input-type="textarea"
                v-if="inputTypes.indexOf('SMS/Text') !== -1"
                no-padding
                no-char-count>
            </labelled-input>
        </form-category>
        <hr>
        <form-category
            section-name="Terms of Agreement"
            icon-name="clipboard-check">
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
        data() {
            return {
                inputTypes: [],
                agreement: false,
            }
        },
        components: {
            'form-category': FormCategory,
            'labelled-input': LabelledInput,
        }
    }
</script>
