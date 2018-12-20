<template>
    <form-template
        :allergens='["milk", "eggs", "soy", "fish", "shellfish", "Peanuts", "wheat"]'
        :preview-text="'preview text'"
        :modalShow="this.modalShow"
        :modalMode="this.modalMode"
        :foodList="this.state.safeFoodList"
        :v="$v"
        @updateState="this.modifyStateBoolean"
        @setState="this.modifyState"
        @submitRequest="this.buildRequest"
        >
    </form-template>
</template>

<script type="text/javascript">
    import FormTemplate from './form-template.vue';
    import Cookies from 'js-cookie';
    import { validationMixin } from "vuelidate"
    import { required, maxLength } from "vuelidate/lib/validators"
    const axios = require('axios');

    export default {
        components: {
            'form-template': FormTemplate,
        },
        methods: {
            modifyStateBoolean(context) {
                this.state[context] = !this.state[context];
            },
            modifyState(context, value) {
                this.state[context] = value;
            },
            buildRequest() {
                var data = {
                     "location": {
                          "main": this.state.location.substring(0, 10),
                          "detail": this.state.location
                     },
                     "event": "Placeholder event",
                     "time": {
                         "created": new Date(),
                         "ended": new Date((new Date()).toString().substring(0,16) + this.state.endTime + ":00")
                     },
                     "food": {
                         "served": this.state.foodEvent,
                         "amount": this.state.foodQuantity,
                         "allergens": this.state.allergens
                     },
                     "bringContainers": this.state.needContainer,
                     "foodServiceInfo": {
                         "permitNumber": this.state.permitNumber,
                         "safeToShareFood": this.state.safeFoodList
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
        computed: {
            modalShow: function() {
                //show the model so long as one of the field sets is incomplete
                return (
                    (!this.state.claimsPermit || !this.state.permitNumber) &&
                    (
                        !this.state.onSafeList ||
                        this.state.safeFoodList.length == 0 ||
                        !this.state.acceptedSafeListTerms
                    )
                );
            },
            modalMode: function() {
                if (this.state.claimsPermit) {
                    return "permit";
                }
                if (this.state.onSafeList) {
                    if (this.state.safeFoodList.length) {
                        return "safeListConfirmation";
                    }
                    return "safeList";
                }
                return "default";
            }
        },
        data() {
            return {
                state: {
                        claimsPermit: false,
                        permitNumber: null,
                        onSafeList: false,
                        safeFoodList: [],
                        acceptedSafeListTerms: false,
                        foodEvent: "",
                        foodQuantity: "",
                        endTime: "",
                        location: "",
                        allergens: [],
                        needContainer: false,
                },
                form : {
                    description: "",
                    quantity: "",
                    time: "",
                    location: ""
                },
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
    }
</script>
