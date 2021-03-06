<template>
    <generic-page
      :startWithNotification="privNotifText != undefined"
      ref="notifBox">
      <template #notification>
          {{privNotifText}}
      </template>
      <template #heading>
          Don't leave people stranded!
      </template>
      <template #body>
          <b-modal id="submitconfirmation" title="Confirmation"
            title-tag="h3"
            ok-title="Send" cancel-variant="outline-secondary"
            @shown="focusMyElement"
            @ok="sendUpdate()">
              <p >
                We will send your update to UW Food Alert Subscribers.
              </p>
              <preview-box>
                  Update:
                  <span v-if="selected == 'noFoodUpdate'">
                    No food left! The event: {{state.event}} has ended and is
                    no longer serving food.
                  </span>
                  <span v-else-if="selected == 'otherUpdate'">
                      {{otherText}}
                  </span>
              </preview-box>
          </b-modal>
          <p class="p pb-3">
            When the food is all gone, please return here to send an update.
            This will prevent people from making unnecessary trips.
          </p>
          <b-form>
            <b-form-radio-group
              v-model="selected" stacked>
              <b-form-radio value="noFoodUpdate"
                @change="validationOn = false">
                  <span>No food left</span>
              </b-form-radio>
              <b-form-radio id="otherRadio"
                value="otherUpdate" class="mt-1" ref="otherUpdate">
                  <span class="mt-2 w-100">
                      Other message
                      <b-form-textarea
                        id="other-message"
                        ref="otherMessage" maxlength="100"
                        aria-label="other message description"
                        required placeholder="We've moved to HUB 120"
                        class="mb-2 standard-placeholder" v-model="otherText"
                        size="lg" @click="selected='otherUpdate'"
                        :state="inputValid()"
                        @blur="validationOn = true">
                      </b-form-textarea>
                      <b-form-invalid-feedback id="other-message-feedback"
                        role="alert">
                        Please describe the update you want to send.
                      </b-form-invalid-feedback>
                  </span>
              </b-form-radio>
            </b-form-radio-group>
          </b-form>
          <h2 class="h2">Preview</h2>
          <preview-box>
            <p v-if="selected == 'otherUpdate' && otherText == ''"
              class="preview-pretext">
                Enter your message above to see a preview of the notification.
            </p>
            <div v-else>
                Update:
                <span v-if="selected == 'noFoodUpdate'">
                  No food left! The event: {{state.event}} has ended and
                  is no longer serving food.
                </span>
                <span v-else-if="selected == 'otherUpdate'">
                    <span> {{otherText}} </span>
                </span>
            </div>
          </preview-box>
      </template>
      <template #navigation>
          <div class="mt-5">
              <b-row align-h="end">
                  <b-col md="3" lg="3">
                    <b-button class="mb-3 button-text" type="submit"
                      block variant="primary" style="white-space: nowrap;"
                      size="lg"
                      @click="preSendUpdate()">
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
      validationOn: false,
    };
  },
  mounted() {
    this.$children[0].$data.showUpdateOverlay = true;

    const headers = {
      'Content-Type': 'application/json',
    };

    axios.get(`/api/v1/notification/?host_netid=${this.netID}`, {headers})
        .then((response) => {
          const data = response.data.filter((notif) => {
            return notif.ended === false;
          });

          if (data.length === 0) {
            this.$router.push({name: 'h-welcome'});
          } else {
            axios.get(`/api/v1/notification/${data[0].id}/`,
                {headers})
                .then((response) => {
                  this.state = response.data;
                  this.$children[0].$data.showUpdateOverlay = false;
                }).catch((error) =>
                  this.showErrorPage(error.response, 'h-update'));
          }
        })
        .catch((error) => this.showErrorPage(error.response, 'h-update'));
  },
  methods: {
    focusMyElement(e) {
      const el = document.getElementById('submitconfirmation');

      el.setAttribute('tabIndex', '-1');
      el.focus();
      el.removeAttribute('tabIndex');
    },
    preSendUpdate() {
      if ((this.otherText === '') && (this.selected !== 'noFoodUpdate')) {
        this.validationOn = true;
        this.$refs.otherMessage.$el.focus();

        return;
      }

      this.$bvModal.show('submitconfirmation');
    },
    sendUpdate() {
      if (this.selected === 'noFoodUpdate') {
        const data = {
          'text': `No Food left! The event: ${this.state.event 
                  } has ended and is no longer serving food`,
          'parent_notification_id': this.state.id,
          'ended': true,
        };
        const csrftoken = Cookies.get('csrftoken');
        const headers = {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        };

        axios.post('/api/v1/updates/', data, {headers})
            .then((response) => {
              this.$router.push({name: 'h-ended'});
            })
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

        axios.post('/api/v1/updates/', data, {headers})
            .then((response) => {
              this.privNotifText = 'Your update was sent.';
              this.$refs.notifBox.notificationState = true;
            })
            .catch((error) => this.showErrorPage(error.response, 'h-update'));
      }

      this.selected = 'noFoodUpdate';
      this.otherText= '';
    },
    inputValid() {
      if (this.validationOn) {
        return (((this.otherText === '') &&
          (this.selected === 'otherUpdate')) ? false : null);
      }

      return null;
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

    .preview-pretext {
      text-align: center;
      font-style: italic;
      margin: auto;
    }
</style>
