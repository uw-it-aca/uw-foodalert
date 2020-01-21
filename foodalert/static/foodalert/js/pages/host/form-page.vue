<template>
  <generic-page>
    <template #heading>
      Compose notification
    </template>
    <template #body>
      <b-modal id="submitconfirmation" title="Confirmation" title-tag="h3"
        ok-title="Send"
        cancel-variant="outline-secondary"
        @shown="focusMyElement"
        @ok="submitAndNext()">
        <p>
          We will send your notification to UW Food Alert Subscribers.
        </p>
        <preview-box>
          <span>{{concatinateMessage()}}</span>
          <br />

          <br />
          End time:
          <span v-if="form.end_time">{{formatedTimeToStr()}}</span>
          <span v-else>--:-- --</span>
          <br />
          Location: <span v-if="form.location">{{form.location}}</span>
          <span v-else>{{placeholderForm.location}}</span>
          <span v-if="form.allergens.length != 0">
            <br />
            May contain:
            <span v-for="(list, index) in form.allergens" :key="list">
              <span>{{list}}</span>
              <span v-if="index+1 < form.allergens.length">, </span>
            </span>
          </span>
          <br />
          <p class="mb-0" v-if="form.bring_container">
            <br />
            You must bring a food storage container.
          </p>
        </preview-box>
      </b-modal>

      <b-form @submit="onSubmit" v-if="show">
        <p class="mb-0">
          Now let's get some details about your food and event so
          you can send a notification.
        </p>

        <div>
          <label class="standard-label w-100 mb-0" for="event-name">
            Event name
            <b-form-input id="event-name" ref="event" maxlength="40"
              v-model="form.event" :state="inputValid('event')"
              :placeholder="placeholderForm.event"
              class="standard-placeholder mt-2"
              size="lg" @blur="enableValidation.event=true">
            </b-form-input>
            <b-form-invalid-feedback id="event-name-feedback" role="alert">
              Please enter an event name.
            </b-form-invalid-feedback>
          </label>
        </div>

        <div>
          <label id="food-label" class="standard-label mb-0 w-100"
            for="food-description">
            Describe the food
            <p id="food-clarification" class="mb-2"
               style="font-size: 14px; font-weight: 400;">
              Tell people about your
              food and the approximate quantity.</p>
            <b-form-textarea id="food-description" ref="food_served"
                            maxlength="200"
                            aria-describedby="food-clarification"
                            v-model="form.food_served"
                            :state="inputValid('food_served')"
                            :placeholder="placeholderForm.food_served"
                            class="standard-placeholder" size="lg"
                            @blur="enableValidation.food_served=true"
                            rows="3"
                            max-rows="8">
            </b-form-textarea>
            <b-form-invalid-feedback id="food-description-feedback"
              role="alert">
              Please enter a description of your food.
            </b-form-invalid-feedback>
          </label>
        </div>

        <div>
          <label id="location-label" class="standard-label w-100 mb-0"
            for="location">Location
            <b-form-input id="location"
              ref="location" maxlength="200"
              v-model="form.location" :state="inputValid('location')"
              :placeholder="placeholderForm.location"
              class="standard-placeholder mt-2" size="lg"
              @blur="enableValidation.location=true">
            </b-form-input>
            <b-form-invalid-feedback id="location-feedback" role="alert">
              Please enter the location of your event.
            </b-form-invalid-feedback>
            </label>
        </div>

        <label class="standard-label mb-0 w-100"
          id="end-time-label" for="end-time">
          End time
          <p id="time-clarification" class="mb-2"
             style="font-size: 14px; font-weight: 400;">
            Set the time when food service will be over.
          </p>
          <b-row>
            <b-col sm=12 md=8>
              <div v-if="isMobile">
                <b-form-input id="end-time" aria-describedby="end-time-feedback"
                  v-model="form.end_time"
                  :state="inputValid('end_time')"
                  type="time" class="standard-placeholder" size="lg">
                </b-form-input>
                <b-form-invalid-feedback id="end-time-feedback" role="alert">
                  Please enter the at which this food service will be over.
                </b-form-invalid-feedback>
              </div>

              <time-picker timeID="end-time" v-model="form.end_time"
                        startWithCurrent labelbyID="end-time-label" v-else>
              </time-picker>
              <b-form-text id="end-time-warning" text-variant="info"
                  style="font-size: 14px; font-weight: 800;"
                  v-if="form.end_time && endTimeBeforeCurrent()">
                  <p> Warning: End Time is before current time. </p>
                  <p> End Time is set to be {{ endTimeBeforeCurrent() }} TOMORROW. </p>
              </b-form-text>
            </b-col>
          </b-row>
        </label>

        <h2 class="h2 pb-0 mb-0">Food specifications</h2>
        <h3 id="allergen-label" class="standard-label mb-0">
          Does the food contain the following allergens?
        </h3>
        <p id="allergen-clarification" class="mb-2" style="font-size: 14px;">
          It's OK if you are unsure, just select to the best of your
          knowledge.
        </p>

        <b-container class="px-0 mx-0">
          <b-form-checkbox-group id="allergens-checkbox"
            v-model="form.allergens"
            aria-describedby="allergen-clarification">
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

        <h3 class="standard-label mb-2" id="bring-label">
          Do people need to bring food storage containers?
        </h3>
        <b-container class="px-0 mx-0">
          <b-form-radio-group id="bring-radio"
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
          <span>{{concatinateMessage()}}</span>
          <br />
          <br />
          End time:
          <span v-if="form.end_time">{{formatedTimeToStr()}}</span>
          <span v-else>--:-- --</span>
          <br />
          Location: <span v-if="form.location">{{form.location}}</span>
          <span v-else>{{placeholderForm.location}}</span>
          <span v-if="form.allergens.length != 0">
            <br />
            May contain:
            <span v-for="(list, index) in form.allergens" :key="list">
              <span>{{list}}</span>
              <span v-if="index+1 < form.allergens.length">, </span>
            </span>
          </span>
          <br />
          <p v-if="form.bring_container" class="mb-0">
            <br />
            You must bring a food storage container.
          </p>
        </preview-box>
        <!--b-card class="mt-3" header="Form Data Result">
                    <pre class="m-0">{{ form }}</pre>
                </b-card!-->

        <div class="mt-5">
          <b-row align-h="end">
            <b-col md="3" lg="3">
              <b-button class="mb-3 button-text" type="submit"
                block variant="primary"
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
  props: {
    food_qualifications: Array,
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
      placeholderForm: {
        location: 'HUB Ballroom',
        event: 'Graduate student social',
        food_served: '3 platters of Mediterranean appetizers:' +
         ' marinated mushrooms, grilled asparagus, caprese salad,' +
         ' cured meats',
      },
      formValidate: {
        event: false,
        food_served: false,
        location: false,
        end_time: true,
        // bring_container: false,
      },
      enableValidation: {
        location: false,
        event: false,
        food_served: false,
        end_time: true,
        // bring_container: false,
      },
      allergens: [],
      show: true,
      isMobile: false,
    };
  },
  methods: {
    focusMyElement(e) {
      const el = document.getElementById('submitconfirmation');

      el.setAttribute('tabIndex', '-1');
      el.focus();
      el.removeAttribute('tabIndex');
    },
    concatinateMessage() {
      let msg = '';

      if (this.form.food_served) {
        msg += this.form.food_served;
      } else {
        msg += this.placeholderForm.food_served;
      }

      msg += ' from ';

      if (this.form.event) {
        msg += this.form.event;
      } else {
        msg += this.placeholderForm.event;
      }

      msg += '.';

      return msg;
    },
    endTimeBeforeCurrent() {
      const splitTime = this.form.end_time.split(/:/);
      const datetime = new Date();

      datetime.setHours(splitTime[0], splitTime[1]);
      console.log(datetime)

      if (datetime < new Date()) {
        return this.formatedTimeToStr();
      }
      return null;
    },
    onSubmit(evt) {
      evt.preventDefault();

      // triping all input validators
      Object.keys(this.enableValidation).forEach(function(key) {
        this.enableValidation[key] = true;
      }.bind(this));

      let flag = false;

      Object.keys(this.formValidate).forEach(function(key) {
        if (this.formValidate[key] === false && flag !== true) {
          flag = true;
          this.$refs[key].$el.focus();
        }
      }.bind(this));

      if (flag) return;

      this.$bvModal.show('submitconfirmation');
    },
    formatedTimeToStr() {
      const splitTime = this.form.end_time.split(/:| /);
      let hours = parseInt(splitTime[0]);
      const mins = splitTime[1];
      let timeExt = 'AM';

      if (hours === 0) {
        hours = 12;
      } else if (hours === 12) {
        timeExt = 'PM'
      } else if (hours > 12) {
        hours -= 12;
        timeExt = 'PM'
      }

      return hours + ':' + mins + ' ' + timeExt;
    },
    submitAndNext() {
      const splitTime = this.form.end_time.split(/:/);
      const datetime = new Date();

      datetime.setHours(splitTime[0], splitTime[1]);

      if (datetime <= new Date()) {
        datetime.setDate(datetime.getDate() + 1);
      }

      const data = {
        'netID': this.netID,
        'location': this.form.location,
        'event': this.form.event,
        'end_time': datetime.toISOString(),
        'food': {
          'served': this.form.food_served,
          'qualifications': this.food_qualifications,
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

      axios.post('/api/v1/notification/', data, {headers})
          .then(function(response) {
            this.$router.push({name: 'h-update', params: {
              notificationText: 'Your notification was sent.',
            }});
          }.bind(this))
          .catch((error) => this.showErrorPage(error.response, 'h-form'));
    },
    inputValid(fieldName) {
      if (this.enableValidation[fieldName]) {
        return (this.formValidate[fieldName] ? null : false);
      }

      return null;
    },
    updateValidity(newState, fieldName, checkFunction) {
      if (newState[fieldName] !== undefined &&
          checkFunction(newState[fieldName])) {
        this.formValidate[fieldName] = true;
        this.enableValidation[fieldName] = true;
      } else {
        this.formValidate[fieldName] = false;
      }
    },
  },
  beforeMount() {
    if (typeof this.food_qualifications === 'undefined') {
      this.$router.push({name: 'h-welcome'});
    }
  },
  mounted() {
    this.isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    this.formValidate.end_time = !this.isMobile;

    this.$children[0].$data.showUpdateOverlay = true;
    const headers = {
      'Content-Type': 'application/json',
    };

    axios.get(
        '/api/v1/notification/?host_netid=' + this.netID,
        {headers},
    ).then((result) => {
      result.data = result.data.filter((d)=>!d.ended);

      if (result.data.length) {
        this.$router.push({name: 'h-update', params: {
          notificationText: 'You already have an event running.',
        }});
      } else {
        this.$children[0].$data.showUpdateOverlay = false;
      }
    }).catch((error) => this.showErrorPage(error.response, 'h-form'));
    axios.get('/api/v1/allergen/', {headers}).then((result) => {
      this.allergens = [];
      result.data.forEach((allergen)=>{
        this.allergens.push(allergen.name);
      });
    }).catch((error) => this.showErrorPage(error.response, 'h-form'));
  },
  watch: {
    form: {
      handler(newState) {
        const checkFunction = (text)=>{
          text = text.trim();

          return text.length > 0;
        };

        this.updateValidity(newState, 'location', checkFunction);
        this.updateValidity(newState, 'event', checkFunction);
        this.updateValidity(newState, 'food_served', checkFunction);
        this.updateValidity(newState, 'end_time',
            (t)=>/^\d{1,2}:\d{2}$/.test(t));
      },
      deep: true,
    },
  },
};
</script>
