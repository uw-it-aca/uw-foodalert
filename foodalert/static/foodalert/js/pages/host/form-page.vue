<template>
    <generic-page>
        <template #heading>
            Compose notification
        </template>
        <template #body>
            <b-modal id="submitconfirmation" title="Confirmation" ok-title="Send" cancel-variant="outline-secondary" @ok="submitAndNext()">
                <p>
                    We will send your notification to Hungry Husky Subscribers.
                </p>
                <preview-box>
                    <span v-if="form.food_served">{{form.food_served}}</span>
                    <span v-else>Hot Indian buffet food</span> from
                    <span v-if="form.event">{{form.event}}</span>
                    <span v-else>FIUTS weekly club meeting</span>.
                    <br/>
                    <br/>
                    Quantity: <span v-if="form.amount_of_food_left">{{form.amount_of_food_left}}</span>
                    <span v-else>About 8 full meals</span>
                    <br/>
                    End time:
                    <span v-if="form.end_time">{{formatedTimeToStr()}}</span>
                    <span v-else>--:-- --</span>
                    <br/>
                    Location: <span v-if="form.location">{{form.location}}</span>
                    <span v-else>HUB 130</span>
                    <span v-if="form.allergens.length != 0">
                        <br />
                        May contain:
                        <span v-for="(list, index) in form.allergens" :key="list">
                            <span>{{list}}</span><span v-if="index+1 < form.allergens.length">, </span>
                        </span>
                    </span>
                    <br/>
                    <p v-if="form.bring_container">
                        <br/>
                        You must bring a food storage container.
                    </p>
                </preview-box>
            </b-modal>

            <b-form @submit="onSubmit" @reset="onReset" v-if="show">
              <p class="mb-0 pb-0">Now let's get some details about your food and event so you can send a notification.</p>
                <label class="standard-label" for="event-name">Event name</label>
                <b-form-input id="event-name" aria-describedby="Name of the event"
                    v-model="form.event" required placeholder="FIUTS weekly club meeting" class="standard-placeholder" size="lg"></b-form-input>

                <label class="standard-label" for="food-description">Describe the food</label>
                <b-form-textarea id="food-description" aria-describedby="Describe the food"
                    v-model="form.food_served" required placeholder="Hot Indian buffet food" class="standard-placeholder" size="lg"></b-form-textarea>

                <label class="standard-label" for="quantity">Quantity</label>
                <b-form-input id="quantity" aria-describedby="Quantity of food"
                    v-model="form.amount_of_food_left" required placeholder="About 8 full meals" class="standard-placeholder" size="lg"></b-form-input>

                <label class="standard-label" for="end-time">End time (when food service will end)</label>
                <b-form-input id="end-time" aria-describedby="End time of the event"
                    v-model="form.end_time" required type="time" class="standard-placeholder" size="lg" v-if="isMobile"></b-form-input>
                <ctk-date-time-picker id="end-time" v-model="form.end_time"
                    class="standard-placeholder" format="hh:mm a" formatted="hh:mm a" :onlyTime="true" :noLabel="true" v-else></ctk-date-time-picker>

                <label class="standard-label" for="location">Location</label>
                <b-form-input id="location" aria-describedby="Location of the event"
                    v-model="form.location" required placeholder="HUB 130" class="standard-placeholder" size="lg"></b-form-input>

                <h2 class="h2 pb-0 mb-0">Food specifications</h2>
                <h5 class="h3 mb-2 pb-0">Does the food contain allergens?</h5>
                <p class="mb-3">It's ok if you are unsure, just select to the best of your knowledge.</p>

                <b-container class="px-0">
                    <b-form-checkbox-group id="allergens-checkbox" v-model="form.allergens">
                        <b-row>
                            <b-col v-for="allergen in allergens" :key="allergen"  cols="6">
                                <b-form-checkbox :value="allergen" class="mb-2">
                                    <span>
                                        {{allergen}}
                                    </span>
                                </b-form-checkbox>
                            </b-col>
                        </b-row>
                    </b-form-checkbox-group>
                </b-container>

                <h5 class="h3">Do people need to bring food storage containers? </h5>
                <b-container class="px-0">
                    <b-form-radio-group id="bring-radio" v-model="form.bring_container" stacked>
                        <b-form-radio :value="true">
                            <span>Yes</span>
                        </b-form-radio>
                        <b-form-radio :value="false" class="mt-1">
                            <span>No</span>
                        </b-form-radio>
                  </b-form-radio-group>
                </b-container>


                <h2 class="h2">Preview</h2>
                <preview-box>
                    <span v-if="form.food_served">{{form.food_served}}</span>
                    <span v-else>Hot Indian buffet food</span> from
                    <span v-if="form.event">{{form.event}}</span>
                    <span v-else>FIUTS weekly club meeting</span>.
                    <br/>
                    <br/>
                    Quantity: <span v-if="form.amount_of_food_left">{{form.amount_of_food_left}}</span>
                    <span v-else>About 8 full meals</span>
                    <br/>
                    End time:
                    <span v-if="form.end_time">{{formatedTimeToStr()}}</span>
                    <span v-else>--:-- --</span>
                    <br/>
                    Location: <span v-if="form.location">{{form.location}}</span>
                    <span v-else>HUB 130</span>
                    <span v-if="form.allergens.length != 0">
                        <br />
                        May contain:
                        <span v-for="(list, index) in form.allergens" :key="list">
                            <span>{{list}}</span><span v-if="index+1 < form.allergens.length">, </span>
                        </span>
                    </span>
                    <br/>
                    <p v-if="form.bring_container">
                        <br/>
                        You must bring a food storage container.
                    </p>
                </preview-box>
                <!--b-card class="mt-3" header="Form Data Result">
                    <pre class="m-0">{{ form }}</pre>
                </b-card!-->

                <div class="mt-5">
                    <b-row align-h="between">
                        <b-col md="5" lg="4" order-md="2">
                        </b-col>
                        <b-col md="5" lg="4" order-md="2"><b-button class="mb-3" type="submit" block variant="primary" size="lg" style="white-space: nowrap;">Submit</b-button>
                        </b-col>
                    </b-row>
                </div>
            </b-form>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
    import Cookies from 'js-cookie';
    import GenericPage from "../../components/generic-page.vue";
    import PreviewBox from "../../components/custom-preview-box.vue";
    import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
    import 'vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';
    const axios = require('axios');

    export default {
        components: {
            "generic-page": GenericPage,
            "preview-box": PreviewBox,
            "ctk-date-time-picker": VueCtkDateTimePicker
        },
        data() {
            return {
                form: {
                    location: "",
                    event: "",
                    end_time: null,
                    food_served: "",
                    amount_of_food_left: "",
                    bring_container: false,
                    safe_foods: [],
                    allergens: [],
                    host_user_agent: "",
                    ended: false
                },
                allergens: [],
                show: true,
                isMobile: false
            }
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()
                this.$bvModal.show("submitconfirmation");
            },
            onReset(evt) {
                evt.preventDefault()
                // Reset our form values
                this.form.location = "",
                this.form.event = "",
                this.form.end_time = null,
                this.form.food_served = "",
                this.form.amount_of_food_left = "",
                this.form.bring_container = false,
                this.form.safe_foods = [],
                this.form.allergens = [],
                this.form.host_user_agent = "",
                this.form.ended = false
            },
            formatedTimeToStr() {
                if (this.isMobile) {
                    var hours = parseInt(this.form.end_time.substr(0,2));
                    var mins = parseInt(this.form.end_time.substr(3,2));
                    var time_ext = "AM"
                    if (hours == 0) {
                        hours = 12;
                    } else if (hours == 12) {
                        time_ext = "PM"
                    } else if (hours > 12) {
                        hours -= 12;
                        time_ext = "PM"
                    }
                    return (hours < 10 ? "0" : "") + hours + ":" + (mins < 10 ? "0" : "") + mins + " " + time_ext;
                }
                return this.form.end_time;
            },
            submitAndNext(){
                var splitTime = this.form.end_time.split(/\:/);
                splitTime[0] = parseInt(splitTime[0])
                // Converting split time to 24 hours format
                if (splitTime[1].split(" ").length != 1) {
                    splitTime[0] += (splitTime[1].split(" ")[1] == "PM") ? 12 : 0
                    splitTime[1] = splitTime[1].split(" ")[0]
                }
                splitTime[1] = parseInt(splitTime[0])

                var datetime = new Date();
                datetime.setHours(splitTime[0], splitTime[1])
                if (datetime < new Date()) {
                    datetime.setDate(datetime.getDate() + 1)
                }

                var data = {
                    "netID": this.netID,
                    "location": this.form.location,
                    "event": this.form.event,
                    "end_time": datetime.toISOString(),
                    "food": {
                        "served": this.form.food_served,
                        "amount": this.form.amount_of_food_left,
                        "allergens": this.form.allergens
                    },
                    "bring_container": this.form.bring_container,
                    "host": {
                        "hostID": this._uid,
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
                        this.$router.push({ name: 'h-update', params: {notificationText: "Your notification was sent."}});
                    }.bind(this))
                    .catch(function (error) {
                        this.$router.push({ name: 'unrecoverable', params: {
                            errorHeading: error.response.statusText,
                            errorMessage: error.response.data[Object.keys(error.response.data)[0]],
                            errorCode: error.response.status,
                            tryAgainPage: "h-form",
                        }});
                    }.bind(this))
            }
        },
        beforeMount() {
            axios.get("/notification/?host_netid=" + this.netID).then((result) => {
                result.data = result.data.filter((d)=>!d.ended)
                if(result.data.length)
                    this.$router.push({ name: 'h-update', params: {notificationText: "You already have an event running."}});
            }).catch(function (error) {
                this.$router.push({ name: 'unrecoverable', params: {
                    errorHeading: error.response.statusText,
                    errorMessage: error.response.data[Object.keys(error.response.data)[0]],
                    errorCode: error.response.status,
                    tryAgainPage: "h-form",
                }});
            }.bind(this));
            axios.get("/allergen/").then((result) => {
                this.allergens = []
                result.data.forEach((allergen)=>{this.allergens.push(allergen.name)});
            }).catch(function (error) {
                this.$router.push({ name: 'unrecoverable', params: {
                    errorHeading: error.response.statusText,
                    errorMessage: error.response.data[Object.keys(error.response.data)[0]],
                    errorCode: error.response.status,
                    tryAgainPage: "h-form",
                }});
            }.bind(this));
            this.form.end_time = new Date().toLocaleTimeString().split(/\:\d\d /).join(" ")
            if (this.form.end_time.length < 8)
                this.form.end_time = "0" + this.form.end_time
        },
        mounted() {
            this.isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        }
    }
</script>
