<template>
  <generic-page>
    <template tabindex="0" #heading>
      Responsibilities
    </template>
    <template #body>
      <p>
        To ensure the safety of the food being shared, we ask that you
        to agree to all of the following requirements.
      </p>
      <b-form-group ref="resForm">
        <b-form-checkbox
          v-model="selected"
          id="cond1"
          class="mt-2"
          value="cond1"
          aria-describedby="condition-feedback"
          :state="inputValid('cond1')"
          @change="addToValidate('cond1')"
          @click.native.capture="stopOnButtonClick">
          <span>
            <span>
              My office is responsible for the safety of the food I am
              sharing.
            </span>
            <div v-if="isIOSDevice">
              <button class="btn btn-link p-0" role="link" v-b-toggle.cond1-info
                aria-label="Learn more about safety responsibilities">
                Learn more
              </button>
            </div>
            <button class="btn btn-link p-0" role="link"
              v-b-toggle.cond1-info v-else
              aria-label="Learn more about safety responsibilities">
              Learn more
            </button>
          </span>
        </b-form-checkbox>
        <collapse-text-box bid="cond1-info">
          You are responsible for food safety under the approval of
          the Temporary Food Permit. This same level of responsibility
          applies when using the UW Food Alert App.
        </collapse-text-box>
        <b-form-checkbox
          v-model="selected"
          id="cond2"
          class="mt-2"
          value="cond2"
          aria-describedby="condition-feedback"
          :state="inputValid('cond2')"
          @change="addToValidate('cond2')"
          @click.native.capture="stopOnButtonClick">
          <span>
            <span>
              Potentially hazardous food must be kept at appropriate
              temperatures and have been sitting out at room temperature
              for no more than <strong>four hours</strong>.
            </span>
            <div v-if="isIOSDevice">
              <button class="btn btn-link p-0" role="link" v-b-toggle.cond2-info
                aria-label="Learn more about potentially hazardous food">
                Learn more
              </button>
            </div>
            <button class="btn btn-link p-0" role="link"
              v-b-toggle.cond2-info v-else
              aria-label="Learn more about potentially hazardous food">
              Learn more
            </button>
          </span>
        </b-form-checkbox>
        <collapse-text-box bid="cond2-info">
            Information is missing
        </collapse-text-box>
        <div class="invalid-feedback pt-2"
              :class="{'super-show': (inputValid('cond1') == false)
                || (inputValid('cond2') == false)}"
              id="condition-feedback"
              role="alert">
          In order to use the service please agree to above
          responsibilities.
        </div>
        <div class="mt-5">
            <b-row align-h="between">
                <b-col md="3" lg="3" order-md="2">
                  <b-button
                    class="mb-3 button-text"
                    size="lg"
                    type="submit"
                    block variant="primary"
                    aria-label="Agree to the selected checkboxes"
                    @click="getNextPage()">
                      Agree
                  </b-button>
                </b-col>
                <b-col md="3" lg="3" order-md="1">
                  <b-button
                    class="hh-back-button button-text"
                    href="#"
                    size="lg" type="submit"
                    block variant="outline-secondary"
                    @click="getBackPage()">
                      Back
                  </b-button>
                </b-col>
            </b-row>
        </div>
      </b-form-group>
    </template>
  </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../../components/generic-page.vue';
import CollapseTextBox from '../../components/collapse-text-box.vue';
const axios = require('axios');

export default {
  components: {
    'generic-page': GenericPage,
    'collapse-text-box': CollapseTextBox,
  },
  props: {
    backPage: {
      type: String,
      default: 'h-food-service',
    },
    food_qualifications: Array,
  },
  methods: {
    getNextPage() {
      this.enableValidation = ['cond1', 'cond2'];

      if (this.selected.length !== 2) {
        return;
      }

      this.$router.push({
        name: 'h-form',
        params: {food_qualifications: this.food_qualifications},
      });
    },
    getBackPage() {
      this.$router.push({name: this.backPage});
    },
    inputValid(fieldValue) {
      if (this.enableValidation.indexOf(fieldValue) !== -1) {
        return (this.selected.indexOf(fieldValue) !== -1 ? null : false);
      }

      return null;
    },
    addToValidate(fieldValue) {
      if (this.enableValidation.indexOf(fieldValue) === -1) {
        this.enableValidation.push(fieldValue);
      }
    },
  },
  data() {
    return {
      selected: [],
      enableValidation: [],
      isIOSDevice: false,
    };
  },
  beforeMount() {
    if (typeof this.food_qualifications === 'undefined') {
      this.$router.push({name: 'h-welcome'});
    }

    const headers = {
      'Content-Type': 'application/json',
    };

    axios.get(
        '/notification/?host_netid=' + this.netID,
        {headers}
    ).then((result) => {
      result.data = result.data.filter((d)=>!d.ended);

      if (result.data.length) {
        this.$router.push({
          name: 'h-update',
          params: {notificationText: 'You already have an event running.'}});
      }
    }).catch((error) =>
      this.showErrorPage(error.response, 'h-responsibilities'));
    this.isIOSDevice = /iPhone|iPod/i.test(navigator.userAgent);
  },
};
</script>
