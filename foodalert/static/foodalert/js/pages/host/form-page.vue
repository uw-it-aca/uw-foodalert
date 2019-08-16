<template>
  <generic-page>
    <template #heading>
      Compose notification
    </template>
    <template #body>
      <b-modal id="submitconfirmation" title="Confirmation" ok-title="Send"
        cancel-variant="outline-secondary"
        @shown="focusMyElement"
        @ok="submitAndNext()">
        <p>
          We will send your notification to Hungry Husky Subscribers.
        </p>
        <preview-box>
          <span v-if="form.food_served">{{form.food_served}}</span>
          <span v-else>Hot Indian buffet food</span> from
          <span v-if="form.event">{{form.event}}</span>
          <span v-else>FIUTS weekly club meeting</span>.
          <br />
          <br />
          Quantity:
          <span v-if="form.amount_of_food_left">
            {{form.amount_of_food_left}}
          </span>
          <span v-else>About 8 full meals</span>
          <br />
          End time:
          <span v-if="form.end_time">{{formatedTimeToStr()}}</span>
          <span v-else>--:-- --</span>
          <br />
          Location: <span v-if="form.location">{{form.location}}</span>
          <span v-else>HUB 130</span>
          <span v-if="form.allergens.length != 0">
            <br />
            May contain:
            <span v-for="(list, index) in form.allergens" :key="list">
              <span>{{list}}</span>
              <span v-if="index+1 < form.allergens.length">, </span>
            </span>
          </span>
          <br />
          <p v-if="form.bring_container">
            <br />
            You must bring a food storage container.
          </p>
        </preview-box>
      </b-modal>

      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <p class="mb-0 pb-1">
          Now let's get some details about your food and event so
          you can send a notification.
        </p>

        <div>
          <label class="standard-label" for="event-name">Event name</label>
          <b-form-input id="event-name" ref="event"
            aria-describedby="event-name-feedback"
            v-model="form.event" :state="inputValid('event')"
            placeholder="FIUTS weekly club meeting"
            class="standard-placeholder"
            size="lg" @blur="enableValidation.event=true">
          </b-form-input>
          <b-form-invalid-feedback id="event-name-feedback">
            Please enter an event name.
          </b-form-invalid-feedback>
        </div>

        <div>
          <label class="standard-label mb-0" for="food-description">
            Describe the food
          </label>
          <p class="mb-2" style="font-size: 15px;">Tell people about your
            food and the approximate quantity.</p>
          <b-form-textarea id="food-description" ref="food_served"
                          aria-describedby="food-description-feedback"
                          v-model="form.food_served"
                          :state="inputValid('food_served')"
                          placeholder="Hot Indian buffet food"
                          class="standard-placeholder" size="lg"
                          @blur="enableValidation.food_served=true">
          </b-form-textarea>
          <b-form-invalid-feedback id="food-description-feedback">
            Please enter a description of your food.
          </b-form-invalid-feedback>
        </div>

        <div>
          <label class="standard-label" for="location">Location</label>
          <b-form-input id="location" aria-describedby="location-feedback"
            ref="location"
            v-model="form.location" :state="inputValid('location')"
            placeholder="HUB 130" class="standard-placeholder" size="lg"
            @blur="enableValidation.location=true">
          </b-form-input>
          <b-form-invalid-feedback id="location-feedback">
            Please enter the location of your event.
          </b-form-invalid-feedback>
        </div>

        <label class="standard-label mb-0" id="end-time-label" for="end-time">
          End time
        </label>
        <p class="mb-2" style="font-size: 14px;">
          Set the time when food service will be over.
        </p>
        <b-row>
          <b-col sm=12 md=8>
            <b-form-input id="end-time" aria-describedby="End time of the event"
              v-model="form.end_time"
              type="time" class="standard-placeholder" size="lg"
              v-if="isMobile"></b-form-input>
            <time-picker timeID="end-time" v-model="form.end_time"
                      startWithCurrent labelbyID="end-time-label" v-else>
            </time-picker>
          </b-col>
        </b-row>

        <h2 class="h2 pb-0 mb-0">Food specifications</h2>
        <h3 id="allergen-label" class="standard-label mb-0">Does the food contain allergens?</h3>
        <p class="mb-2" style="font-size: 14px;">
          It's ok if you are unsure, just select to the best of your
          knowledge.
        </p>

        <b-container class="px-0">
          <b-form-checkbox-group id="allergens-checkbox"
            v-model="form.allergens" aria-labelledby="allergen-label">
            <b-row>
              <b-col v-for="allergen in allergens" :key="allergen" cols="6">
                <b-form-checkbox :value="allergen" class="mb-2">
                  <span>
                    {{allergen}}
                  </span>
                </b-form-checkbox>
              </b-col>
            </b-row>
          </b-form-checkbox-group>
        </b-container>

        <h3 class="standard-label mb-2" id="bring-label">Do people need to bring food storage containers? </h3>
        <b-container class="px-0">
          <b-form-radio-group id="bring-radio" aria-labelledby="bring-label"
            v-model="form.bring_container" stacked>
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
          <br />
          <br />
          Quantity:
          <span v-if="form.amount_of_food_left">
            {{form.amount_of_food_left}}
          </span>
          <span v-else>About 8 full meals</span>
          <br />
          End time:
          <span v-if="form.end_time">{{formatedTimeToStr()}}</span>
          <span v-else>--:-- --</span>
          <br />
          Location: <span v-if="form.location">{{form.location}}</span>
          <span v-else>HUB 130</span>
          <span v-if="form.allergens.length != 0">
            <br />
            May contain:
            <span v-for="(list, index) in form.allergens" :key="list">
              <span>{{list}}</span>
              <span v-if="index+1 < form.allergens.length">, </span>
            </span>
          </span>
          <br />
          <p v-if="form.bring_container">
            <br />
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
            <b-col md="5" lg="4" order-md="2">
              <b-button class="mb-3" type="submit" block variant="primary"
                size="lg" style="white-space: nowrap;">
                Submit
              </b-button>
            </b-col>
          </b-row>
        </div>
      </b-form>
    </template>
  </generic-page>
</template>

<script type="text/javascript">
import Cookies from 'js-cookie';
import GenericPage from '../../components/generic-page.vue';
import PreviewBox from '../../components/custom-preview-box.vue';
import TimePicker from '../../components/time-picker.vue';
const axios = require('axios');

export default {
  components: {
    'generic-page': GenericPage,
    'preview-box': PreviewBox,
    'time-picker': TimePicker,
  },
  data() {
    return {
      form: {
        location: '',
        event: '',
        end_time: null,
        food_served: '',
        bring_container: false,
        allergens: [],
        host_user_agent: '',
      },
      formValidate: {
        event: false,
        food_served: false,
        location: false,
        //end_time: false,
        //bring_container: false,
      },
      enableValidation: {
        location: false,
        event: false,
        //end_time: false,
        food_served: false,
        //bring_container: false,
      },
      allergens: [],
      show: true,
      isMobile: false,
    };
  },
  methods: {
    focusMyElement(e) {
      let el = document.getElementById('submitconfirmation')
      el.setAttribute("tabIndex", "-1");
      el.focus();
      el.removeAttribute("tabIndex")
    },
    onSubmit(evt) {
      evt.preventDefault();

      // triping all input validators
      Object.keys(this.enableValidation).forEach(function (key) {
        this.enableValidation[key] = true
      }.bind(this));

      var flag = false
      Object.keys(this.formValidate).forEach(function (key) {
        if (this.formValidate[key] == false && flag != true) {
          flag = true
          console.log(key)
          this.$refs[key].$el.focus()
        }
      }.bind(this));

      if (flag) return;

      this.$bvModal.show('submitconfirmation');
    },
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.location = '',
      this.form.event = '',
      this.form.end_time = null,
      this.form.food_served = '',
      this.form.amount_of_food_left = '',
      this.form.bring_container = false,
      this.form.safe_foods = [],
      this.form.allergens = [],
      this.form.host_user_agent = ''
    },
    formatedTimeToStr() {
      if (this.isMobile) {
        let hours = parseInt(this.form.end_time.substr(0, 2));
        const mins = parseInt(this.form.end_time.substr(3, 2));
        let timeExt = 'AM';
        if (hours == 0) {
          hours = 12;
        } else if (hours == 12) {
          timeExt = 'PM';
        } else if (hours > 12) {
          hours -= 12;
          timeExt = 'PM';
        }
        return (hours < 10 ? '0' : '') + hours + ':' +
          (mins < 10 ? '0' : '') + mins + ' ' + timeExt;
      }
      return this.form.end_time;
    },
    submitAndNext() {
      const splitTime = this.form.end_time.split(/\:/);
      splitTime[0] = parseInt(splitTime[0]);
      // Converting split time to 24 hours format
      if (splitTime[1].split(' ').length != 1) {
        splitTime[0] += (splitTime[1].split(' ')[1] == 'PM') ? 12 : 0;
        splitTime[1] = splitTime[1].split(' ')[0];
      }
      splitTime[1] = parseInt(splitTime[0]);

      const datetime = new Date();
      datetime.setHours(splitTime[0], splitTime[1]);
      if (datetime < new Date()) {
        datetime.setDate(datetime.getDate() + 1);
      }

      const data = {
        'netID': this.netID,
        'location': this.form.location,
        'event': this.form.event,
        'end_time': datetime.toISOString(),
        'food': {
          'served': this.form.food_served,
          'amount': "test amount",
          'allergens': this.form.allergens,
        },
        'bring_container': this.form.bring_container,
        'host': {
          'hostID': this._uid,
          'userAgent': navigator.userAgent,
        },
      };

      const csrftoken = Cookies.get('csrftoken');
      const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      };
      axios.post('/notification/', data, {'headers': headers})
          .then(function(response) {
            this.$router.push({name: 'h-update', params: {
              notificationText: 'Your notification was sent.',
            }});
          }.bind(this))
          .catch((error) => this.showErrorPage(error.response, 'h-form'));
    },
    inputValid(fieldName) {
      if (this.enableValidation[fieldName])
        return (this.formValidate[fieldName] ? null : false)
      return null;
    },
    updateValidity(newState, fieldName, length) {
      if (newState[fieldName] != undefined && newState[fieldName].length > length) {
        this.formValidate[fieldName] = true
        this.enableValidation[fieldName] = true
      } else {
        this.formValidate[fieldName] = false
      }
    }
  },
  beforeMount() {
    axios.get('/notification/?host_netid=' + this.netID).then((result) => {
      result.data = result.data.filter((d)=>!d.ended);
      if (result.data.length) {
        this.$router.push({name: 'h-update', params: {
          notificationText: 'You already have an event running.',
        }});
      }
    }).catch((error) => this.showErrorPage(error.response, 'h-form'));
    axios.get('/allergen/').then((result) => {
      this.allergens = [];
      result.data.forEach((allergen)=>{
        this.allergens.push(allergen.name);
      });
    }).catch((error) => this.showErrorPage(error.response, 'h-form'));
  },
  mounted() {
    this.isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
  },
  watch: {
    form: {
      handler(newState) {
        this.updateValidity(newState, "location", 0);
        this.updateValidity(newState, "event", 0);
        this.updateValidity(newState, "food_served", 0);
      },
      deep: true
    }
  }
};
</script>
