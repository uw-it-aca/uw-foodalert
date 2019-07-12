<template>
    <generic-page :startWithNotification="privNotifText != undefined" ref="notifBox">
        <template #notification>
            {{privNotifText}}
        </template>
        <template #heading>
            Compose update
        </template>
        <template #body>
            <b-modal id="submitconfirmation" title="Confirmation" @ok="sendUpdate()">
                <p>
                    We will send your update to Hungry Husky Subscribers.
                </p>
                <preview-box>
                    Update:
                    <span v-if="selected == 'noFoodUpdate'"> No food left at {{state.location}} </span>
                    <span v-else-if="selected == 'otherUpdate'">
                        <span v-if="otherText == ''"> We've moved to HUB 120 </span>
                        <span v-else> {{otherText}} </span>
                    </span>.
                    Re: {{state.food.served}} leftover from {{state.event}}...
                </preview-box>
            </b-modal>
            <h2 class="h2">Don't leave people stranded!</h2>
            <p class="p">
                When the food is all gone, please return here to send an update. This will prevent people making unnecessary trips.
            </p>
            <b-form>
                <b-form-radio-group stacked v-model="selected">
                    <b-form-radio value="noFoodUpdate">
                        <span>No food left</span>
                    </b-form-radio>
                    <b-form-radio id="otherRadio" value="otherUpdate">
                        <span>
                            Other Message
                            <b-form-input id="other-message" aria-describedby="Other message for the subs"
                            required placeholder="We've moved to HUB 120" class="mb-3" v-model="otherText">
                            </b-form-input>
                        </span>
                    </b-form-radio>
                </b-form-radio-group>
            </b-form>
            <h2 class="h2 mt-4">Preview</h2>
            <preview-box>
                Update:
                <span v-if="selected == 'noFoodUpdate'"> No food left at {{state.location}} </span>
                <span v-else-if="selected == 'otherUpdate'">
                    <span v-if="otherText == ''"> We've moved to HUB 120 </span>
                    <span v-else> {{otherText}} </span>
                </span>.
                Re: {{state.food.served}} leftover from {{state.event}}...
            </preview-box>
        </template>
        <template #navigation>
            <div class="mt-5">
                <b-row align-h="between">
                    <b-col md="5" lg="4" order-md="2"><b-button class="mb-3" type="submit" block variant="primary" style="white-space: nowrap;" @click="$bvModal.show('submitconfirmation')" :disabled="(otherText == '') && (selected != 'noFoodUpdate')">Send Update</b-button>
                    </b-col>
                </b-row>
            </div>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
    import GenericPage from "../../components/generic-page.vue";
    import PreviewBox from "../../components/custom-preview-box.vue";
    import CustomRadio from "../../components/custom-radio.vue";
    import Cookies from 'js-cookie';
    const axios = require('axios');

    export default {
        components:{
            "generic-page": GenericPage,
            "preview-box": PreviewBox,
            "custom-radio": CustomRadio,
        },
        props: {
            notificationText: String,
        },
        data() {
            return {
                selected: "noFoodUpdate",
                state: {
                    food: {
                        served: "",
                    },
                    event: "",
                    location: "",
                },
                otherText: "",
                privNotifText: this.notificationText,
            }
        },
        beforeCreate() {
            var headers = {
                    'Content-Type': 'application/json',
                }
            axios.get('/notification/', {"headers": headers})
                .then(response => {
                    var data = response.data.filter(function(notif) {
                        return notif.ended == false;
                    });
                    if (data.length === 0) {
                        this.$router.push({ name: 'h-form'});
                    } else {
                        this.state = data[0]
                    }
                    this.state.uid = this._uid;
                })
                .catch(error => {
                    console.log("There was an error processing the request");
                    console.log(error);
                })
        },
        methods: {
            sendUpdate() {
                if (this.selected == "noFoodUpdate") {
                    var data = {
                        "text": "No Food left! The event: " + this.state.event + " has ended and is no longer serving food",
                        "parent_notification": this.state.id
                    };
                    var csrftoken = Cookies.get('csrftoken');
                    var headers = {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    };

                    axios.post('/updates/', data, {"headers": headers})
                        .then(function(response) {
                            console.log(response);
                        }.bind(this))
                        .catch(function (error) {
                            console.log("There was an error processing the request");
                            console.log(error);
                        })

                    var data = {
                        "ended": true,
                    };

                    axios.patch("/notification/" + this.state.id + "/", data, {"headers": headers})
                        .then(response => {
                            console.log(response);
                            this.$router.push({ name: 'h-ended' });
                        })
                        .catch(error => {
                            console.log(error);
                        })
                } else {
                    var data = {
                        "text": this.otherText,
                        "parent_notification": this.state.id
                    };
                    var csrftoken = Cookies.get('csrftoken');
                    var headers = {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    }
                    axios.post('/updates/', data, {"headers": headers})
                        .then(function(response) {
                            console.log(response)
                            this.privNotifText = "Your update was sent.";
                            this.$refs.notifBox.showNotification()
                        }.bind(this))
                        .catch(function (error) {
                            console.log("There was an error processing the request");
                            console.log(error);
                        })
                }
                this.selected = "noFoodUpdate";
                this.otherText= "";
            },
        },
    }
</script>

<style>
    #otherRadio label {
        margin-top: 5px;
    }

    .h2 {
      font-size: 22px !important;
      font-weight: 600 !important;
      line-height: 1.375 !important;
      color: #484848 !important;
    }

    .p {
      font-size: 16px !important;
      font-weight: 400 !important;
      line-height: 1.375 !important;
      color: #484848 !important;
    }

    #other-message {
        margin-top: 10px;
    }
</style>
