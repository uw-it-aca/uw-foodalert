<template>
    <signup-template
    :v="$v"
    @updateInput="this.updateInput"
    >
    </signup-template>
</template>

<script type="text/javascript">
    import SignupTemplate from './signup-template.vue';
    import { validationMixin } from "vuelidate"
    import { required, email, helpers } from "vuelidate/lib/validators"
    const phoneNum = helpers.regex('phoneNum', /^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/)

    export default {
        components: {
            'signup-template': SignupTemplate,
        },
        methods: {
            updateInput(value) {
                this.inputTypes = value;
            },
        },
        data() {
            return {
                inputTypes: [],
                form: {
                    email: "",
                    sms: ""
                },
            }
        },
        validations() {
            if (this.inputTypes.indexOf('SMS/Text') !== -1 && this.inputTypes.indexOf('Email') !== -1) {
                return {
                    form: {
                        email: {
                            required,
                            email
                        },
                        sms: {
                            required,
                            phoneNum
                        }
                    }
                }
            } else if (this.inputTypes.indexOf('SMS/Text') == -1 && this.inputTypes.indexOf('Email') !== -1) {
                return {
                    form: {
                        email: {
                            required,
                            email
                        },
                        sms: {

                        }
                    }
                }
            } else if (this.inputTypes.indexOf('SMS/Text') !== -1 && this.inputTypes.indexOf('Email') == -1) {
                return {
                    form: {
                        sms: {
                            required,
                            phoneNum
                        },
                        email: {

                        }
                    }
                }
            } else {
                return {
                    form: {
                        email: {

                        },
                        sms: {

                        }
                    }
                }
            }
        },
    }   
</script>

