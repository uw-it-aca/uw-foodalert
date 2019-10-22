<template>
  <generic-page>
    <template tabindex="0" #heading>
      Food service information
    </template>
    <template #body>
      <p>
        Let’s determine whether your food can be shared with the public.
        Please select all that apply.
      </p>
      <b-form-group>
        <b-form-checkbox v-model="selected" value="preparedByAuth"
                         aria-labelledby="catering-option"
                         @change="uncheckCheckbox(2)">
          <span id="catering-option">
            My food was prepared by UW Housing &amp;
            Food Services or Bay Laurel Catering.
          </span>
        </b-form-checkbox>
        <b-form-checkbox v-model="selected" class="mt-2" value="hasPermit"
                         aria-labelledby="permit-option"
                         @change="uncheckCheckbox(2)"
                         @click.native.capture="stopOnButtonClick">
          <span id="permit-option">
            I have a UW Temporary Food Service Permit.
            <div v-if="isIOSDevice">
              <button class="btn btn-link p-0" role="link"
                v-b-toggle.perm-info
              aria-label="Learn more about UW Temporary Food Service Permit">
                Learn more
              </button>
            </div>
            <button class="btn btn-link p-0" role="link" v-b-toggle.perm-info
              v-else
              aria-label="Learn more about UW Temporary Food Service Permit">
              Learn more
            </button>
          </span>
        </b-form-checkbox>
        <collapse-text-box bid="perm-info">
          When providing food to the public (anyone beyond the staff or
          faculty of your unit), UW offices are required to secure a
          Temporary Food Permit through
          <a href="https://www.ehs.washington.edu/workplace/food-safety-program/temporary-food-service-permit"
          target="_blank" aria-label="UW Environmental Health &amp; Safety
          Temporary Food Service Permit page"> UW Environmental Health &amp;
          Safety </a> to help ensure that food service providers
          meet safety regulations and the food itself is safe for consumption.
        </collapse-text-box>
        <b-form-checkbox v-model="selected" value="none" class="mt-2"
          aria-describedby="none-apply"
          @change="uncheckCheckbox(0); uncheckCheckbox(1)">
          <span id="none-apply">
            None of these apply.
          </span>
        </b-form-checkbox>
        <div class="invalid-feedback pt-2"
             :class="{'super-show': selected.length == 0 && validateOn}"
              id="food-service-feedback"
              role="alert">
          <span aria-hidden="true">
            Please select at least one option to move on.
          </span>
          <span class="sr-only" role="presentation" unSelectable="on">
            Please select at least one option to move on.
            Please navigate back up to the checkboxes
          </span>
        </div>
      </b-form-group>
    </template>
    <template #navigation>
      <div class="mt-5">
        <b-row align-h="between">
          <b-col md="3" lg="3" order-md="2">
            <b-button class="mb-3 button-text" type="submit" block size="lg"
              variant="primary" @click="getNextPage()"
              aria-label="Continue and submit selected checkboxes">
              Continue
            </b-button>
          </b-col>
          <b-col md="3" lg="3" order-md="1">
            <b-button class="hh-back-button button-text" type="submit" block
              href="#"
              size="lg" variant="outline-secondary"
              @click="getBackPage()">Back</b-button>
          </b-col>
        </b-row>
      </div>
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
    bid: String,
  },
  methods: {
    getNextPage() {
      if (this.selected.length === 0) {
        this.validateOn = false;
        setTimeout(function() {
          this.validateOn = true;
        }.bind(this), 1);

        return;
      }

      if (this.selected.includes('hasPermit') ||
        this.selected.includes('preparedByAuth')) {
        this.$router.push({
          name: 'h-responsibilities',
          params: {
            backPage: 'h-food-service',
            food_qualifications: this.selected,
          },
        });
      } else {
        this.$router.push({name: 'h-categories'});
      }
    },
    getBackPage() {
      this.$router.push({name: 'h-welcome'});
    },
    uncheckCheckbox(pos) {
      setTimeout(function() {
        document.querySelectorAll('input')[pos].checked = false;
        this.selected = this.selected.filter((val) => {
          return val !== document.querySelectorAll('input')[pos]._value;
        });

        if (!this.validateOn) this.validateOn = true;
      }.bind(this), 1);
    },
  },
  data() {
    return {
      selected: [],
      validateOn: false,
      isIOSDevice: false,
    };
  },
  mounted() {
    this.$children[0].$data.showUpdateOverlay = true;
    const headers = {
      'Content-Type': 'application/json',
    };

    axios.get(
        '/notification/?host_netid=' + this.netID,
        {headers}
    ).then((result) => {
      result.data = result.data.filter((d)=>!d.ended);

      if (result.data.length) {
        this.$router.push({name: 'h-update', params: {
          notificationText: 'You already have an event running.',
        }});
      } else {
        this.$children[0].$data.showUpdateOverlay = false;
      }
    }).catch((error) => this.showErrorPage(error.response, 'h-food-service'));
    this.isIOSDevice = /iPhone|iPod/i.test(navigator.userAgent);
  },
};
</script>
