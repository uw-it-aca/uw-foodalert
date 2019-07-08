<template>
    <generic-page>
        <template #heading>
            Compose Notification
        </template>
        <template #body>
            <b-modal id="submitconfirmation" title="Confirmation" @ok="submitAndNext()">
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
                    <br/>
                    May contain:
                    <span v-for="(list, index) in form.allergens">
                        <span>{{list}}</span><span v-if="index+1 < form.allergens.length">, </span>
                    </span>
                    <br/>
                    <p v-if="form.bring_container">
                        <br/>
                        You must bring food storage container.
                    </p>
                </preview-box>
            </b-modal>

            <b-form @submit="onSubmit" @reset="onReset" v-if="show">
                <label class="standard-label" for="event-name">Event name</label>
                <b-form-input id="event-name" aria-describedby="Name of the event"
                    v-model="form.event" required placeholder="FIUTS weekly club meeting" class="mb-4 standard-placeholder"></b-form-input>

                <label class="standard-label" for="food-description">Describe the food</label>
                <b-form-textarea id="food-description" aria-describedby="Describe the food"
                    v-model="form.food_served" required placeholder="Hot Indian buffet food" class="mb-4"></b-form-textarea>

                <label class="standard-label" for="quantity">Quantity</label>
                <b-form-input id="quantity" aria-describedby="Quantity of food"
                    v-model="form.amount_of_food_left" required placeholder="About 8 full meals" class="mb-4"></b-form-input>

                <label class="standard-label" for="end-time">End Time</label>
                <b-form-input id="end-time" aria-describedby="End time of the event"
                    v-model="form.end_time" required type="time" class="mb-4"></b-form-input>

                <label class="standard-label" for="location">Location</label>
                <b-form-input id="location" aria-describedby="Location of the event"
                    v-model="form.location" required placeholder="e.g HUB 130" class="mb-4"></b-form-input>

                <h2 class="mt-4 h2">Food Specifications</h2>
                <h5 class="standard-label">Does the food contain allergens?</h5>
                <p class="p">It's ok if you are unsure, just select to the best of your knowledge.</p>

                <b-container>
                    <b-form-checkbox-group id="allergens-checkbox" v-model="form.allergens">
                        <b-row>
                            <b-col v-for="allergen in allergens" sm="6">
                                <b-form-checkbox :value="allergen">{{allergen}}</b-form-checkbox>
                            </b-col>
                        </b-row>
                    </b-form-checkbox-group>
                </b-container>

                <h5 class="mt-4 standard-label">Do students need to bring food storage containers? </h5>
                <b-container>
                    <b-form-radio-group id="bring-radio" v-model="form.bring_container">
                        <b-row>
                            <b-col sm="3">
                                <b-form-radio :value="true">Yes</b-form-radio>
                            </b-col>
                            <b-col sm="3">
                                <b-form-radio :value="false">No</b-form-radio>
                            </b-col>
                        </b-row>
                    </b-form-radio-group>
                </b-container>

                <h2 class="mt-4">Preview</h2>
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
                    <br/>
                    May contain:
                    <span v-for="(list, index) in form.allergens">
                        <span>{{list}}</span><span v-if="index+1 < form.allergens.length">, </span>
                    </span>
                    <br/>
                    <p v-if="form.bring_container">
                        <br/>
                        You must bring a container.
                    </p>
                </preview-box>
                <!--b-card class="mt-3" header="Form Data Result">
                    <pre class="m-0">{{ form }}</pre>
                </b-card!-->

                <div class="mt-5">
                    <b-row align-h="between">
                        <b-col md="5" lg="4" order-md="2"><b-button class="mb-3" type="submit" block variant="primary" size="lg" style="white-space: nowrap;">Submit</b-button>
                        </b-col>
                        <b-col md="5" lg="4" order-md="1"><b-button class="mb-3" type="reset" block variant="danger" size="lg" style="white-space: nowrap;">Reset</b-button></b-col>
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
    const axios = require('axios');

    export default {
        components: {
            "generic-page": GenericPage,
            "preview-box": PreviewBox,
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
                show: true
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
            formatedTimeToStr(){
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
            },
            submitAndNext(){
                var data = {
                     "location": this.form.location,
                     "event": this.form.event,
                     "time": {
                         "created": new Date(),
                         "ended": new Date((new Date()).toString().substring(0,16) + this.form.end_time + ":00")
                     },
                     "food": {
                         "served": this.form.food_served,
                         "amount": this.form.amount_of_food_left,
                         "allergens": this.form.allergens
                     },
                     "bringContainers": this.form.bring_container,
                     "foodServiceInfo": {
                         "safeToShareFood": this.form.safe_foods
                     },
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
                        alert("There was an error processing the request");
                        console.log(error);
                    })
            }
        },
        beforeCreate() {
            axios.get("/notification/").then((result) => {
                result.data = result.data.filter((d)=>!d.ended)
                if(result.data.length)
                    this.$router.push({ name: 'h-update', params: {notificationText: "You already have an event running."}});
            });
            console.log(this.$router.history.current.name);
        },
        beforeMount() {
            axios.get("/allergen/").then((result) => {
                this.allergens = []
                result.data.forEach((allergen)=>{this.allergens.push(allergen.name)});
            });
        },
    }
</script>
<style>
  .standard-label {
    font-size: 16px !important;
    font-weight: 600 !important;
    line-height: 1.375 !important;
    color: #6B6C72;
  }

  .standard-placeholder {
    font-size: 16px !important;
    font-weight: 400 !important;
    color: #484848 !important;
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
</style>
