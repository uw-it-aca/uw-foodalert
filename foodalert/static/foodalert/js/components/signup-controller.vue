<template>
    <signup-template
        :v="$v"
        v-bind.sync="this.val"
        @send="this.send"/>
</template>

<script type="text/javascript">
    import Cookies from 'js-cookie';
    import axios from 'axios';
    import SignupTemplate from './signup-template.vue';
    import { validationMixin } from "vuelidate"
    import { requiredIf, email, helpers } from "vuelidate/lib/validators"
    const phoneNum = helpers.regex('phoneNum', /^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/)
    //a function that takes a validator and a predicate and checks the validator
    //only if the predicate is true, function is curried (i.e must be called
    //checkIf(validator)(predicate))
    const checkIf = (check) => (predicate) => (value) => predicate() ? check(value) : true;

    export default {
        components: {
            'signup-template': SignupTemplate,
        },
        data() {
            return {
                val: {
                    inputTypes: [],
                    email: "",
                    sms: "",
                    agreement: false,
                }
            }
        },
        computed: {
            reqBody: function() {
                var ret = {};
                ret['email'] = this.val.email;
                ret['sms_number'] = this.val.sms;
                ret['netId'] = '';
                return ret;
            },
        },
        methods: {
            send() {
                var csrftoken = Cookies.get('csrftoken');
                var headers = {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                };
                axios.post('/subscription/', this.reqBody, {"headers": headers})
                    .then(console.log);
            },
        },
        validations() {
            return {
                val: {
                    email: {
                        requiredIf: requiredIf(function(v) {
                            return this.val.inputTypes.indexOf('Email') !== -1
                        }),
                        emailIf: checkIf(email)((v) => {
                            return this.val.inputTypes.indexOf('Email') !== -1
                        })
                    },
                    sms: {
                        requiredIf: requiredIf(function(v) {
                            return this.val.inputTypes.indexOf('SMS/Text') !== -1
                        }),
                        phoneNumIf: checkIf(phoneNum)((v) => {
                            return this.val.inputTypes.indexOf('SMS/Text') !== -1
                        })
                    }
                }
            }
        },
    }
</script>
