<template>
  <b-card no-body class="notif-option-card">
    <b-container slot="header" class="p-0">
      <b-row>
        <b-col cols="8">
          <slot name="opt_heading">Placeholder Text</slot>
          <br/>
          <br/>
          {{email}}
          <slot name="disclaimer">Placeholder disclaimer</slot>
        </b-col>
        <b-col cols="4">
          <b-form-checkbox v-model="checked"
            name="email-enable-switch"
            class="float-right mr-3"
            aria-label="email-switch"
            switch>
          </b-form-checkbox>
        </b-col>
      </b-row>
    </b-container>
  </b-card>
</template>

<script>
const axios = require('axios');

import Cookies from 'js-cookie';

export default {
  props: {
    email: String,
    subid: Number,
    requestUpdate: Function,
  },
  data() {
    return {
      // variables for switch
      disableNotif: false,
      checked: false,
    };
  },
  methods: {
    createSubscription() {
      // create Subscription model with uw email
      axios.get('/subscription/?netID=' + this.netID)
          .then((response) => {
            if (!response.data[0]) {
              const csrftoken = Cookies.get('csrftoken');
              const headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
              };
              const postData = {
                'email': this.netID + '@uw.edu',
                'sms_number': '',
              };

              axios.post('/subscription/', postData, {headers})
                  .then((response) => {
                    this.requestUpdate();
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
  watch: {
    checked(newVal, oldVal) {
      // change email_notif value
      const data = {
        'send_email': newVal,
      };
      const csrftoken = Cookies.get('csrftoken');
      const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      };
      const url = '/subscription/' + this.subid + '/';

      axios.patch(url, data, {headers})
          .catch((error) => {
            this.showErrorPage(error.response, 's-notifications');
          });
    },
  },
  beforeMount() {
    this.createSubscription();
  },
};
</script>

<style>
    .notif-option-card .card-header{
        background-color: inherit;
        border-bottom: none;
        padding-left: 0;
        padding-right: 0;
    }
    .notif-option-card .text-muted{
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .notif-option-card .card-body{
        padding: 0;
        padding-bottom: 10px;
    }
    .notif-option-card .form-group{
        margin-bottom: -10px;
    }
    .notif-option-card .opt_link_btn {
        text-align: right;
    }
    .notif-option-card .toggle_link_btn {
        text-align: left;
    }
    .notif-option-card.notif-option-card {
        border-radius: 0;
        border: unset;
        border-top: 1px solid #9B9B9B;
        border-bottom: 1px solid #9B9B9B;
        padding-top: 12px;
        padding-bottom: 14px;
    }
    .notif-option-card~.notif-option-card{
        border-top: unset;
    }
    .notif-option-card input.form-control~small {
        margin-top: 1px;
    }
    .notif-option-card .slide-fade-enter-active {
        transition: all 1s ease;
    }
    .notif-option-card .slide-fade-leave-active {
        transition: all 1s cubic-bezier(1.0, 0.5, 0.8, 1.0);
    }

    .notif-option-card .text-unverified {
        color: #E05018;
    }

    .notif-option-card .text-verified {
        color: #1C834B;
    }

    .notif-option-card .form-text.error-desp {
        color: #E05018;
    }

    .notif-option-card .spinner-padding {
        margin-bottom: .125rem;
    }

    .notif-option-card .spinner-hide {
        display: none;
    }

    .notif-option-card .notif-option-heading {
        font-size: 18px;
        font-weight: 600;
        line-height: 1.375;
        -moz-osx-font-smoothing: grayscale;
        /*margin-top: 12px;*/
    }

    .notif-option-card .notif-option-heading
    .btn.opt_link_btn.btn-link.btn-block {
        font-size: 18px;
        font-weight: 600;
        line-height: 1.375;
        -moz-osx-font-smoothing: grayscale;
        /*margin-top: 12px;*/
    }
</style>
