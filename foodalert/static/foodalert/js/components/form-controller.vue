<template>
    <form-template
        :allergens='["milk", "eggs", "soy", "fish", "shellfish", "Peanuts", "wheat"]'
        :preview-text="previewText"
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
                     "location": this.state.location,
                     "event": this.state.event,
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
                    .then(function(response) {
                        console.log(response);
                        this.$router.push({ name: 'permit'});
                    }.bind(this))
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
                    (!this.state.claimsPermit || !this.state.event) &&
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
            },
            previewText: function() {
                var foods = this.state.foodEvent;
                //Add in foods from the safe food list if it was used
                if (this.state.onSafeList) {
                    foods += " ";
                    for (var food in this.state.safeFoodList) {
                        foods += this.state.safeFoodList[food] + ", ";
                    }
                    foods = foods.slice(0, -2);
                }
                //Change the end time into readable format
                var time = "Ends At: "
                if (this.state.endTime != "") {
                    var hour = parseInt(this.state.endTime.substring(0,2));
                    if (hour > 12) {
                        time += (hour - 12) + this.state.endTime.substring(2,5) + " PM";
                    } else if (hour == 12) {
                        time += this.state.endTime + " PM"
                    } else if (hour == 0) {
                        time += "12" + this.state.endTime.substring(2,5) + " AM"
                    } else {
                        time += this.state.endTime + " AM";
                    }
                }

                var text =  { 'heading': "An event has just been posted! Here are the details...",
                              'food': "Food Served: " + foods,
                              'location': "Location: " + this.state.location,
                              'quantity': "Amount Left: " + this.state.foodQuantity,
                              'time': time,
                              };
                //Add in any allergens if they were selected
                if (this.state.allergens.length > 0) {
                    var allergens = "Food Contains: ";
                    for (var food in this.state.allergens) {
                        allergens += this.state.allergens[food] + ", ";
                    }
                    text.allergens = allergens.slice(0, -2);
                }
                //Add an additional message if containers are required
                if (this.state.needContainer) {
                    text.container = "Please Bring A Container!";
                }
                return text;
            }
        },
        data() {
            return {
                state: {
                        claimsPermit: false,
                        onSafeList: false,
                        safeFoodList: [],
                        acceptedSafeListTerms: false,
                        foodEvent: "",
                        foodQuantity: "",
                        endTime: "",
                        location: "",
                        allergens: [],
                        needContainer: false,
                        notificationID: 0,
                        event: "",
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
