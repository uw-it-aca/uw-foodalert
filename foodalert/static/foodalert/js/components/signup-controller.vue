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
    import { parsePhoneNumberFromString } from 'libphonenumber-js'
    const phoneNum = function(s) {
        if (s === '') {
            return true;
        }

        try {
            return parsePhoneNumberFromString(s, 'US').isValid();
        } catch (e) {
            return false;
        }
    }
    //a function that takes a validator and a predicate and checks the validator
    //only if the predicate is true, function is curried (i.e must be called
    //checkIf(validator)(predicate))
    const checkIf = (check) => (predicate) => (value) => predicate() ? check(value) : true;

    export default {
        props: {
            subId: Number
        },
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

                if(this.val.inputTypes.indexOf('Email') !== -1) {
                    ret['email'] = this.val.email;
                }

                if(this.val.inputTypes.indexOf('SMS/Text') !== -1) {
                    try {
                        ret['sms_number'] = parsePhoneNumberFromString(
                            this.val.sms, 'US').number;
                    } catch (error) {
                        ret['sms_number'] = '';
                    }
                }

                return ret;
            },
        },
        watch: {
            val: {
                inputTypes: function(arr, old) {
                    $v.$reset();
                    $v.$touch();
                }
            }
        },
        methods: {
            send() {
                var csrftoken = Cookies.get('csrftoken');
                var headers = {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                };
                axios.post('/subscription/', this.reqBody, {"headers": headers})
                    .then(() => this.$router.push('subscribed'));
            },
            update() {
                axios.get(`/subscription/${this.subId}`)
                    .then(resp => resp.data)
                    .then(data => {
                        this.val.email = data.email;
                        if(data.email) {
                            this.val.inputTypes.push('Email');
                        }
                        this.val.sms = data.sms_number;
                        if(data.sms_number) {
                            this.val.inputTypes.push('SMS/Text');
                        }
                    })
            }
        },
        validations() {
            return {
                val: {
                    email: {
                        requiredIf: requiredIf(function(v) {
                            return this.val.inputTypes.indexOf('Email') !== -1
                        }),
                        emailIf: checkIf(email) ((v) => {
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
        beforeRouteEnter(to, from , next) {
            next(vm => vm.update());
        },
        beforeRouteUpdate(to, from , next) {
            this.update();
            next();
        }
    }
</script>
