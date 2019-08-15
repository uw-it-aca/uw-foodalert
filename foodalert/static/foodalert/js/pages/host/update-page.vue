<template>
    <generic-page
      :startWithNotification="privNotifText != undefined"
      ref="notifBox">
      <template #notification>
          {{privNotifText}}
      </template>
      <template #heading>
          Compose update
      </template>
      <template #body>
          <b-modal id="submitconfirmation" title="Confirmation"
            ok-title="Send" cancel-variant="outline-secondary"
            @shown="focusMyElement"
            @ok="sendUpdate()">
              <p tabIndex="-1" ref="focusThis">
                We will send your update to Hungry Husky Subscribers.
              </p>
              <preview-box>
                  Update:
                  <span v-if="selected == 'noFoodUpdate'">
                    No food left at {{state.location}}
                  </span>
                  <span v-else-if="selected == 'otherUpdate'">
                      <span v-if="otherText == ''">
                        We've moved to HUB 120
                      </span>
                      <span v-else> {{otherText}} </span>
                  </span>.
                  Re: {{state.food.served}} leftover from {{state.event}}...
              </preview-box>
          </b-modal>
          <h2 class="h2 pt-0">Don't leave people stranded!</h2>
          <p class="p pb-3">
            When the food is all gone, please return here to send an update.
            This will prevent people from making unnecessary trips.
          </p>
          <b-form>
            <b-form-radio-group stacked v-model="selected">
              <b-form-radio value="noFoodUpdate">
                  <span>No food left</span>
              </b-form-radio>
              <b-form-radio id="otherRadio" value="otherUpdate" class="mt-1"
                ref="otherUpdate">
                  <span class="mt-2 w-100">
                      Other message
                      <b-form-textarea
                        id="other-message"
                        aria-describedby="Other message for the subs"
                        required placeholder="We've moved to HUB 120"
                        class="mb-3 standard-placeholder" v-model="otherText"
                        size="lg" @focus="selected='otherUpdate'">
                      </b-form-textarea>
                  </span>
              </b-form-radio>
            </b-form-radio-group>
          </b-form>
          <h2 class="h2">Preview</h2>
          <preview-box>
              Update:
              <span v-if="selected == 'noFoodUpdate'">
                No food left at {{state.location}}
              </span>
              <span v-else-if="selected == 'otherUpdate'">
                  <span v-if="otherText == ''"> We've moved to HUB 120 </span>
                  <span v-else> {{otherText}}</span>
              </span>.
              Re: {{state.food.served}} leftover from {{state.event}}...
          </preview-box>
      </template>
      <template #navigation>
          <div class="mt-5">
              <b-row align-h="end">
                  <b-col md="5" lg="4" order-md="2">
                    <b-button class="mb-3" type="submit"
                      block variant="primary" style="white-space: nowrap;"
                      size="lg"
                      @click="$bvModal.show('submitconfirmation')"
                      :disabled="(otherText == '') &&
                      (selected != 'noFoodUpdate')">
                        Send Update
                    </b-button>
                  </b-col>
              </b-row>
          </div>
      </template>
    </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../../components/generic-page.vue';
import PreviewBox from '../../components/custom-preview-box.vue';
import Cookies from 'js-cookie';
const axios = require('axios');

export default {
  components: {
    'generic-page': GenericPage,
    'preview-box': PreviewBox,
  },
  props: {
    notificationText: String,
  },
  data() {
    return {
      selected: 'noFoodUpdate',
      state: {
        food: {
          served: '',
        },
        event: '',
        location: '',
      },
      otherText: '',
      privNotifText: this.notificationText,
    };
  },
  beforeMount() {
    const headers = {
      'Content-Type': 'application/json',
    };
    axios.get('/notification/?host_netid=' + this.netID, {'headers': headers})
        .then((response) => {
          const data = response.data.filter(function(notif) {
            return notif.ended == false;
          });
          if (data.length === 0) {
            this.$router.push({name: 'h-welcome'});
          } else {
            axios.get('/notification/' + data[0]['id'] + '/',
                {'headers': headers})
                .then((response) => {
                  console.log(response.data);
                  this.state = response.data;
                }).catch((error) =>
                  this.showErrorPage(error.response, 'h-update'));
          }
        })
        .catch((error) => this.showErrorPage(error.response, 'h-update'));
  },
  methods: {
    focusMyElement(e) {
      this.$refs.focusThis.focus();
    },
    sendUpdate() {
      if (this.selected == 'noFoodUpdate') {
        const data = {
          'text': 'No Food left! The event: ' + this.state.event +
                  ' has ended and is no longer serving food',
          'parent_notification_id': this.state.id,
          'ended': true,
        };
        const csrftoken = Cookies.get('csrftoken');
        const headers = {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        };

        axios.post('/updates/', data, {'headers': headers})
            .then(function(response) {
              console.log(response);
              this.$router.push({name: 'h-ended'});
            }.bind(this))
            .catch((error) => this.showErrorPage(error.response, 'h-update'));
      } else {
        const data = {
          'text': this.otherText,
          'parent_notification_id': this.state.id,
        };
        const csrftoken = Cookies.get('csrftoken');
        const headers = {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        };
        axios.post('/updates/', data, {'headers': headers})
            .then(function(response) {
              console.log(response);
              this.privNotifText = 'Your update was sent.';
              this.$refs.notifBox.showNotification();
            }.bind(this))
            .catch((error) => this.showErrorPage(error.response, 'h-update'));
      }
      this.selected = 'noFoodUpdate';
      this.otherText= '';
    },
  },
};
</script>

<style>
    #otherRadio label {
        margin-top: 5px;
    }

    #other-message {
        margin-top: 10px;
    }
</style>
