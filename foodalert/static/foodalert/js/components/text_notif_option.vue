<template>
  <b-card no-body class="notif-option-card">
    <b-container slot="header" class="p-0">
      <b-row>
        <b-col cols="8">
          <strong>Text</strong>
          <!-- verified state-->
          <span v-if="serverData.text != ''">
            &#xb7;
            <span v-if="!serverData.verified" class="text-unverified">
              Unverified
            </span>
            <span v-else-if="serverData.verified" class="text-verified">
              Verified
            </span>
          </span>
          <!-- end of verified state -->

          <!-- uncollapsed view of text notif component -->
          <div v-if="!isOpen">
            <!-- verified uncollapsed view -->
            <div v-if="serverData.verified" class="pt-1">
                <span class="m-auto">
                  {{serverData.text}}
                  <button v-b-toggle="accord_id" role="link"
                    class="verified_link_btn btn btn-link px-0"
                    :aria-label="'Edit ' + type"
                    :disabled="serverData.twilio_stop">
                    Edit
                  </button>
                </span>
                <slot v-if="serverData.twilio_stop" name="twilio-warning">
                </slot>
            </div>
            <!-- end of verified uncollapsed view -->

            <!-- unverified uncollapsed view -->
            <div v-else>
                <br/>
                <!-- no number view -->
                <div v-if="serverData.text === ''">
                  <b-button block href="#" v-b-toggle="accord_id" variant="link"
                    class="toggle_link_btn p-0" v-if="serverData.text == ''">
                    Add number
                  </b-button>
                </div>
                <!-- end of no number view -->

                <!-- number entered view -->
                <div v-else>
                  <slot v-if="serverData.text !== ''" name="unverifNotifText">
                  </slot>
                  <small class="form-text pt-2 pb-0 error-desp"
                          v-if="errorDesc != ''">
                          {{errorDesc}}
                  </small>
                  <br />
                  <b-button block href="#" v-b-toggle="accord_id" variant="link"
                    @click="updateMode=localData.verified"
                    class="toggle_link_btn p-0"
                    :aria-label="'Edit ' + type">
                    Edit
                  </b-button>
                  <b-button variant="link"
                            @click="getNewState(spinners.resend)"
                            class="px-0">
                    Resend {{type}}
                    <b-spinner small class="mr-2 spinner-padding"
                          :class="{'spinner-hide': !spinners.resend.state}">
                    </b-spinner>
                  </b-button>
                </div>
                <!-- end of number entered view -->
            </div>
            <!-- end of unverified uncollapse view -->
          </div>
        </b-col>
        <!-- right side controls -->
        <b-col cols="4">
          <div v-if="!isOpen">
            <b-form-checkbox v-model="serverData.send_sms"
                  @change="check($event)"
                  :name="type+'enable-switch'"
                  class="float-right mr-3"
                  :aria-label="'enable  '+type"
                  :disabled="!serverData.verified || serverData.twilio_stop"
                  switch>
            </b-form-checkbox>
          </div>
          <div v-else>
            <b-button v-if="serverData.text !== '' || updateMode"
                      block href="#" variant="link"
                      class="opt_link_btn p-0"
                      v-b-toggle="accord_id"
                      @click="updateMode=false; validateOn=false;
                      localData.text=''"
                      :aria-label="'Cancel ' + type">
              Cancel
            </b-button>
            <b-button v-else
                      block href="#" variant="link"
                      class="opt_link_btn p-0"
                      v-b-toggle="accord_id"
                      :aria-label="'Cancel ' + type">
              Cancel
            </b-button>
          </div>
        </b-col>
        <!-- end of right side controls -->
      </b-row>
    </b-container>

    <!-- collapse view -->
    <b-collapse :id="accord_id" accordion="my-accordion"
                role="tabpanel" v-model="isOpen" @show="focusCollapse">
      <b-card-body>
        <b-container class="p-0">
          <b-row>
            <b-col cols="12">
              <b-card-text>
                <!-- new number form -->
                <b-form v-if="serverData.text == ''"
                        @submit.prevent="getNewState(spinners.verify);
                        updateMode=false">
                  <slot name="disclaimer"></slot>
                  <label :for="type+'-add-input'"
                         class="form-text text-muted pt-3 pb-0">
                         <strong>{{label}}</strong>
                  </label>
                  <b-form-group :description="description">
                    <b-form-input required :type="type" :formatter="formatter"
                                  v-model="localData.text" width="300px"
                                  :id="type+'-add-input'">
                    </b-form-input>
                    <div class="invalid-feedback pt-2"
                        :class="{'super-show':validateOn}"
                        :id="type+'-verify-feedback'"
                        role="alert" aria-live="polite">
                      <span aria-hidden="true">
                        {{errorMsg}}
                      </span>
                    </div>
                  </b-form-group>
                  <small class="form-text pt-2 pb-0 error-desp"
                         v-if="errorDesc != ''">
                          {{errorDesc}}
                  </small>
                  <b-button type="submit" variant="primary"
                            class="float-right mt-2 px-3"
                            :aria-label="'Verify ' + type">
                    <b-spinner small class="mr-2 spinner-padding"
                            :class="{'spinner-hide': !spinners.verify.state}">
                    </b-spinner>
                    Verify
                  </b-button>
                </b-form>
                <!-- end of new number form -->

                <!-- update number form -->
                <b-form v-else
                        @submit.prevent="getNewState(spinners.update)"
                        @reset.prevent="deleteData(spinners.delete)">
                  <slot name="update-note"></slot>
                  <slot name="disclaimer"></slot>
                  <label :for="type+'-update-input'"
                    class="form-text text-muted pt-3 pb-0">
                      <strong>{{label}}</strong>
                  </label>
                  <b-form-group :description="description">
                    <b-form-input required :type="type"
                                  :formatter="formatter"
                                  v-model="localData.text"
                                  :id="type+'-update-input'"
                                  width="300px">
                    </b-form-input>
                    <div class="invalid-feedback pt-2"
                      :class="{'super-show': validateOn}"
                      :id="type+'-verify-feedback'"
                      role="alert">
                      <span aria-hidden="true">
                        {{errorMsg}}
                      </span>
                    </div>
                  </b-form-group>
                  <small class="form-text pt-2 pb-0 error-desp"
                          v-if="errorDesc != ''">
                          {{errorDesc}}
                  </small>
                  <b-button type="submit" variant="primary"
                            class="float-right mt-2 ml-2 px-3"
                            :aria-label="'Update ' + type">
                    <b-spinner small class="mr-2 spinner-padding"
                      :class="{'spinner-hide': !spinners.update.state}">
                    </b-spinner>
                    Update
                  </b-button>
                  <b-button type="reset" variant="danger"
                            class="float-right mt-2 ml-2 px-3"
                            :aria-label="'Delete ' + type">
                    <b-spinner small class="mr-2 spinner-padding"
                      :class="{'spinner-hide': !spinners.delete.state}">
                    </b-spinner>
                    Delete
                  </b-button>
                </b-form>
                <!-- end of update number form -->
              </b-card-text>
            </b-col>
          </b-row>
        </b-container>
      </b-card-body>
    </b-collapse>
    <!-- end of collapse view -->
  </b-card>
</template>

<script>
const axios = require('axios');

import Cookies from 'js-cookie';
import {parsePhoneNumber, ParseError, AsYouType}
  from 'libphonenumber-js';

export default {
  props: {
    accord_id: String,
    label: {
      type: String,
    },
    description: {
      type: String,
      default: ' ',
    },
    type: {
      type: String,
    },
    visible: Boolean,
    serverData: Object,
    requestUpdate: Function,
    subid: Number,
  },
  data() {
    return {
      localData: {
        text: '',
        verified: false,
        send_sms: false,
      },
      spinners: {
        cancel: {state: false},
        verify: {state: false},
        resend: {state: false},
        update: {state: false},
        delete: {state: false},
      },
      isOpen: false,
      updateMode: false,
      errorDesc: '',
      validateOn: false,
      errorMsg: '',
    };
  },
  methods: {
    focusCollapse() {
      let input = '';

      if (this.serverData.text === '') {
        input = this.type + '-add-input';
      } else {
        input = this.type + '-update-input';
      }

      const el = document.getElementById(input);

      if (el) {
        el.focus();
      }
    },
    formatter(value, event) {
      if (this.type === 'text') {
        return this.numberFormatter(value, event);
      } else if (this.type === 'email') {
        return value;
      }
    },
    numberFormatter(value, event) {
      if (value === '1' || value === '0') {
        value = '';
      }

      if (this.validateOn) {
        try {
          const phoneNum = parsePhoneNumber(value, 'US');

          if (phoneNum.isValid()) {
            this.validateOn = false;
          }
        } catch (error) {
          if (error instanceof ParseError) {
            // can alter the error message as user types
          } else {
            throw error;
          }
        }
      }

      if (value.length > 14) {
        return value.substr(0, 14);
      }

      if (value.length > 0) {
        if (value.length === 4 &&
          event.inputType === 'deleteContentBackward') {
          value = value.substr(0, 3);
        }

        value = new AsYouType('US').input(value);
      }

      return value;
    },
    getNewState(spinnerOpt) {
      this.validateOn = false;
      // initially true
      let validInput = true;
      let inputType = this.type;
      let notifValue = this.localData.text;

      if (inputType === 'text') {
        inputType = 'sms_number';

        if (notifValue !== '') {
          try {
            const phoneNum = parsePhoneNumber(notifValue, 'US');

            notifValue=phoneNum.number;
            validInput = phoneNum.isValid();
          } catch (error) {
            validInput = false;
          }
        }
      }

      const data = new FormData();

      data.set(inputType, notifValue);
      const csrftoken = Cookies.get('csrftoken');
      const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      };

      spinnerOpt.state = true;

      // make patch request if subid is set; post if not
      if (validInput) {
        if (this.subid) {
          const url = '/api/v1/subscription/' + this.subid + '/';

          axios.patch(url, data, {headers})
              .then((response) => {
                this.requestUpdate();
                spinnerOpt.state = false;

                if (this.newData) {
                  this.newData = false;
                }

                this.updateMode = false;
                this.isOpen=false;
              })
              .catch((error) => {
                spinnerOpt.state = false;
                this.handleInvalidInput(error);
              });
        } else {
          const postData = {
            'email': '',
            'sms_number': '',
          };

          postData[inputType] = notifValue;
          axios.post('/api/v1/subscription/', postData, {headers})
              .then((response) => {
                this.requestUpdate();

                spinnerOpt.state = false;

                if (this.newData) {
                  this.newData = false;
                }

                this.updateMode = false;
                this.isOpen=false;
              })
              .catch((error) => {
                spinnerOpt.state = false;
                this.showErrorPage(error.response,
                    's-notifications');
              });
        }
      } else {
        // show error message
        this.handleInvalidInput(spinnerOpt);
      }
    },
    handleInvalidInput(spinnerOpt) {
      // error should be displayed on page if invalid
      // phone number is entered
      let input = this.type;

      if (this.type === 'text') {
        input = 'phone number';
      }

      this.errorMsg = 'Invalid ' + input + '. Please enter a new one';
      spinnerOpt.state = false;
      this.validateOn = true;
    },
    deleteData(spinnerOpt) {
      this.localData.text = '';
      this.getNewState(spinnerOpt);
    },
    check(event) {
      const data = {
        'send_sms': event,
      };
      const csrftoken = Cookies.get('csrftoken');
      const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      };
      const url = '/api/v1/subscription/' + this.subid + '/';

      axios.patch(url, data, {headers})
          .then(this.requestUpdate)
          .catch((error) => {
            this.showErrorPage(error.response, 's-notifications');
          });
    },
  },
  watch: {
    serverData(newVal, oldVal) {
      this.localData.text = newVal.text; // this is inputting sms with +1
      this.localData.verified = newVal.verified;
    },
  },
  beforeMount() {
    this.localData.text = this.serverData.text;
    this.localData.verified = this.serverData.verified;
    this.isOpen = this.visible;
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
    .notif-option-card .verified_link_btn {
      text-align: left;
      margin-left: 8px;
      display: inline;
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
        color: #D93900;
    }

    .notif-option-card .text-verified {
        color: #1C834B;
    }

    .notif-option-card .form-text.error-desp {
        color: #D93900;
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
