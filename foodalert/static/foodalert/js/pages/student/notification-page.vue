<template>
  <generic-page>
    <template #heading>
      Notification preferences
    </template>
    <template #body>
      <p>
        Select how you will like to receive notifications.
        Please choose at least one.
      </p>
      <text-notif accord_id="text" type="text"
        label="Enter a phone number" :subid="subid"
        :serverData="{ text: notif_info.sms_number,
          verified: notif_info.number_verified,
          send_sms: notif_info.send_sms}"
        :requestUpdate="requestUpdate"
        errorDesc="Carrier rates may apply">
        <template #disclaimer>
          Only US numbers are supported at this time. Carrier rates may apply.
        </template>
        <template #update-note>
          Remove or update your phone number.
        </template>
        <template #unverifNotifText>
          We sent a verification text to {{notif_info.sms_number}}.
          Please reply YES to finish signup.
          <br />
        </template>
      </text-notif>

      <email-notif accord_id="email" type="email"
        label="Enter an email" :subid="subid"
        :requestUpdate="requestUpdate"
        :serverData="{send_email: notif_info.send_email}"
        :email="netID+'@uw.edu'">
        <template #disclaimer>
          <p>Only UW NetIDs are supported at this time</p>
        </template>
      </email-notif>

    </template>
  </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../../components/generic-page.vue';
import TextNotif from '../../components/text_notif_option.vue';
import EmailNotif from '../../components/email_notif_option.vue';
import {AsYouType} from 'libphonenumber-js';
const axios = require('axios');

import Cookies from 'js-cookie';


export default {
  components: {
    'generic-page': GenericPage,
    'text-notif': TextNotif,
    'email-notif': EmailNotif,
  },
  props: {
    bid: String,
    agree: Boolean,
  },
  data() {
    return {
      collapse_notif: false,
      notif_info: {
        email: '',
        email_verified: false,
        send_email: false,
        sms_number: '',
        number_verified: false,
        send_sms: false,
      },
      subid: undefined,
    };
  },
  methods: {
    getSubID(response) {
      if (response.data[0]) {
        this.subid = response.data[0].id;
      }

      return this.subid;
    },
    stripSms(data) {
      // strips sms of the +1
      if (data['sms_number']) {
        let num = data['sms_number'];

        num = num.replace('+1', '');
        num = new AsYouType('US').input(num);
        data['sms_number'] = num;
      }

      return data;
    },
    requestUpdate() {
      const headers = {
        'Content-Type': 'application/json',
      };

      // check if user has agreed to responsibilities
      if (!this.agree) {
        this.$router.push({name: 's-welcome'});

        return;
      }

      axios.get('/api/v1/subscription/?netID=' + this.netID, {headers})
          .then(this.getSubID)
          .then((data) => {
            if (this.subid) {
              const url = '/api/v1/subscription/' + this.subid + '/';

              axios.get(url, {headers})
                  .then((response) => {
                    response.data = this.stripSms(response.data);
                    this.notif_info = response.data;
                    this.$children[0].$data.showUpdateOverlay = false;
                  })
                  .catch((error) =>
                    this.showErrorPage(error.response, 's-notifications'));
            } else {
              // create subscription with email if it does not exist
              const csrftoken = Cookies.get('csrftoken');
              const postHeaders = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
              };
              const postData = {
                'email': this.netID + '@uw.edu',
                'sms_number': '',
              };

              axios.post(
                  '/api/v1/subscription/',
                  postData,
                  {'headers': postHeaders},
              )
                  .then((response) => {
                    this.subid = response.data.id;
                    this.$children[0].$data.showUpdateOverlay = false;
                  })
                  .catch((error) => {
                    this.showErrorPage(error.response,
                        's-notifications');
                  });
            }
          })
          .catch((error) => {
            this.showErrorPage(error.response, 's-notifications');
          });
    },
  },
  mounted() {
    this.$children[0].$data.showUpdateOverlay = true;
    this.requestUpdate();
  },
};
</script>

<style>
    .notification #notif-status .enabled {
        color: green;
    }

    .notification #notif-status .paused {
        color: red;
    }
    .notification .container {
        padding: .75rem 1.25rem;
        padding-left: 0px;
        border-top: 1px solid #9B9B9B;
    }
    .notif-disabled {
        opacity: 0.5;
    }
</style>
