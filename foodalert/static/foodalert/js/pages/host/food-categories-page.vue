<template>
    <generic-page>
        <template #heading>
            Tell us more about your food
        </template>
        <template #body>
            <p>
              The following will help determine whether your food can be
              shared with the public.
            </p>
            <b-form-group>
                <b-form-checkbox
                    v-model="selected"
                    value="non-perishable"
                    @change="uncheckCheckbox(3); uncheckCheckbox(2)">
                    <span>
                        My food is non-perishable.
                        <div v-if="isIOSDevice">
                          <b-link herf="#" v-b-toggle.non-perishable>
                            Examples
                          </b-link>
                        </div>
                        <b-link herf="#" v-b-toggle.non-perishable v-else>
                          Examples
                        </b-link>
                    </span>
                </b-form-checkbox>
                <collapse-text-box bid="non-perishable">
                  Candy, beverages (pasteurized, canned, or bottled),
                  chips, dips.
                </collapse-text-box>
                <b-form-checkbox
                    v-model="selected"
                    class="mt-2"
                    value="pre-packaged"
                    @change="uncheckCheckbox(3); uncheckCheckbox(2)">
                    <span>
                        My food was commercially pre-packaged.
                        <div v-if="isIOSDevice">
                          <b-link herf="#" v-b-toggle.pre-packaged>
                            Examples
                          </b-link>
                        </div>
                        <b-link herf="#" v-b-toggle.pre-packaged>
                          Examples
                        </b-link>
                    </span>
                </b-form-checkbox>
                <collapse-text-box bid="pre-packaged">
                    Wrapped or boxed baked goods (cakes, pies),
                    chips, store-bought ice cream.
                </collapse-text-box>
                <b-form-checkbox
                    v-model="selected"
                    class="mt-2"
                    value="at-home"
                    @change="uncheckCheckbox(0); uncheckCheckbox(1);
                      uncheckCheckbox(3)">
                    My food was prepared at home.
                </b-form-checkbox>
                <b-form-checkbox
                    v-model="selected"
                    class="mt-2"
                    value="none"
                    @change="uncheckCheckbox(0); uncheckCheckbox(1);
                      uncheckCheckbox(2)">
                    <span>
                        None of the above.
                    </span>
                </b-form-checkbox>
                <div class="invalid-feedback pt-2"
                     :class="{'super-show': selected.length == 0 && validateOn}"
                     id="food-service-feedback">
                  Please select at least one option to move on.
                </div>
            </b-form-group>
        </template>
        <template #navigation>
            <div class="mt-5">
               <b-row align-h="between">
                 <b-col md="4" lg="3" order-md="2">
                   <b-button
                    class="mb-3"
                    type="submit"
                    block size="lg"
                    variant="primary"
                    @click="getNextPage()">
                      Continue
                   </b-button>
                 </b-col>
                 <b-col md="4" lg="3" order-md="1">
                    <b-button
                      class="hh-back-button"
                      type="submit" block size="lg"
                      variant="outline-secondary"
                      @click="getBackPage()">
                        Back
                    </b-button>
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
      if (this.selected.length == 0) {
        this.validateOn = true
        return
      }

      if (this.selected.includes('non-perishable') ||
          this.selected.includes('pre-packaged')) {
        this.$router.push({name: 'h-responsibilities'});
      } else if (this.selected.includes('at-home')) {
        this.$router.push({name: 'h-close'});
      } else {
        this.$router.push({name: 'h-need-permit'});
      }
    },
    getBackPage() {
      this.$router.push({name: 'h-food-service'});
    },
    uncheckCheckbox(pos) {
      setTimeout(function() {
        document.querySelectorAll('input')[pos].checked = false
        this.selected = this.selected.filter((val) => {
          return val != document.querySelectorAll('input')[pos]._value
        })
        if (!this.validateOn) this.validateOn = true
      }.bind(this), 100)
    },
  },
  data() {
    return {
      selected: [],
      validateOn: false,
      isIOSDevice: false,
    };
  },
  beforeMount() {
    axios.get('/notification/?host_netid=' + this.netID).then((result) => {
      result.data = result.data.filter((d)=>!d.ended);
      if (result.data.length) {
        this.$router.push({
          name: 'h-update',
          params: {notificationText: 'You already have an event running.'}});
      }
    }).catch((error) => this.showErrorPage(error.response, 'h-categories'));
    this.isIOSDevice = /iPhone|iPod/i.test(navigator.userAgent);
  },
};
</script>
