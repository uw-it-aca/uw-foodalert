<template>
    <b-card no-body class="notif-option-card">
        <b-container slot="header" class="p-0">
            <b-row>
                <b-col cols="8">
                    <slot name="opt_heading">Placeholder Text</slot> 
                    <span v-if="serverData.text != ''">
                        &#xb7; 
                        <span v-if="!serverData.verified" class="text-unverified"> 
                            Unverified
                        </span>
                        <span v-else-if="serverData.verified" class="text-verified"> 
                            Verified
                        </span>
                    </span>
                    <div v-if="serverData.verified" class="pt-1">
                        {{serverData.text}}
                    </div>
                </b-col>
                <b-col cols="4">
                    <div v-if="!isOpen">
                        <b-button block href="#" v-b-toggle="accord_id" variant="link"
                                class="opt_link_btn p-0" v-if="serverData.text == ''">
                            Add
                        </b-button>
                        <b-button block href="#" v-b-toggle="accord_id" variant="link"
                                class="opt_link_btn p-0" @click="updateMode=localData.verified" v-else>
                            Edit
                        </b-button>
                    </div>
                    <div v-else>
                        <b-button block href="#" variant="link" class="opt_link_btn p-0" v-b-toggle="accord_id" @click="localData.text = ''; updateMode=false" v-if="serverData.text == '' || updateMode">
                            <b-spinner small class="mr-2 spinner-padding" :class="{'spinner-hide': !spinners.cancel.state}" ></b-spinner>
                            <slot name="opt_cancel">Cancel</slot>
                        </b-button>
                        <b-button block href="#" variant="link" class="opt_link_btn p-0" @click="cancelUpdate($event, spinners.cancel)" v-else>
                            <b-spinner small class="mr-2 spinner-padding" :class="{'spinner-hide': !spinners.cancel.state}" ></b-spinner>
                            <slot name="opt_cancel">Cancel</slot>
                        </b-button>
                    </div>
                </b-col>
            </b-row>
        </b-container>
        <b-collapse :id="accord_id" accordion="my-accordion" role="tabpanel" v-model="isOpen">
            <b-card-body>
                <b-container class="p-0">
                    <b-row>
                        <b-col cols="12">
                            <b-card-text>
                                <b-form @submit.prevent="getNewState(spinners.verify)" v-if="serverData.text == ''">
                                    <small class="form-text text-muted pt-0">{{label}}</small>
                                    <b-form-group :description="description">
                                        <b-form-input required :type="type" :formatter="formatter" v-model="localData.text" width="300px"></b-form-input>
                                    </b-form-group>
                                    <small class="form-text pt-2 pb-0 error-desp" v-if="errorDesc != ''">{{errorDesc}}</small>
                                    <b-button type="submit" variant="primary" class="float-right mt-2 px-3">
                                        <b-spinner small class="mr-2 spinner-padding" :class="{'spinner-hide': !spinners.verify.state}"></b-spinner>
                                        Verify
                                    </b-button>
                                </b-form>
                                <div v-else-if="!serverData.Unverified">
                                    <div v-if="!updateMode">
                                        <slot name="unverifNotifText" :switchToUpdate="()=>{updateMode = true}">
                                        </slot>
                                        <small class="form-text pt-2 pb-0 error-desp" v-if="errorDesc != ''">{{errorDesc}}</small>
                                        <br />
                                        <b-button variant="link" @click="resendVerif(spinners.resend)" class="px-0">
                                            Resend {{type}}
                                            <b-spinner small class="mr-2 spinner-padding" :class="{'spinner-hide': !spinners.resend.state}"></b-spinner>
                                        </b-button>
                                    </div>
                                    <b-form @submit.prevent="getNewState(spinners.update)" @reset.prevent="deleteData(spinners.delete)" v-else>
                                        <small class="form-text text-muted">{{label}}</small>
                                        <b-form-group :description="description">
                                            <b-form-input required :type="type" :formatter="formatter" v-model="localData.text" width="300px"></b-form-input>
                                        </b-form-group>
                                        <small class="form-text pt-2 pb-0 error-desp" v-if="errorDesc != ''">{{errorDesc}}</small>
                                        <b-button type="submit" variant="primary" class="float-right mt-2 ml-2 px-3">
                                            <b-spinner small class="mr-2 spinner-padding" :class="{'spinner-hide': !spinners.update.state}"></b-spinner>
                                            Update
                                        </b-button>
                                        <b-button type="reset" variant="danger" class="float-right mt-2 ml-2 px-3">
                                            <b-spinner small class="mr-2 spinner-padding" :class="{'spinner-hide': !spinners.delete.state}"></b-spinner>
                                            Delete
                                        </b-button>
                                    </b-form>
                                </div>
                            </b-card-text>
                        </b-col>
                    </b-row>
                </b-container>
            </b-card-body>
        </b-collapse>
    </b-card>
</template>

<script>
    const axios = require('axios');
    import Cookies from 'js-cookie';

    export default {
        props: {
            accord_id: String,
            label: {
                type: String,
                default: "Placeholder label",
            },
            description: {
                type: String,
                default: "Placeholder description",
            },
            type: {
                type: String,
                default: "text"
            },
            visible: Boolean,
            serverData: Object,
            requestUpdate: Function,
            resendVerif: Function,
        },
        data() {
            return {
                localData: {
                    text: "",
                    verified: false,
                },
                spinners: {
                    cancel: { state: false },
                    verify: { state: false },
                    resend: { state: false },
                    update: { state: false },
                    delete: { state: false },
                },
                isOpen: false,
                updateMode: false,
                errorDesc: "",

                notif_input: "",
            } 
        },
        methods: {
            formatter(value, event){
                if (this.type == "text") {
                    return this.numberFormatter(value, event);
                } else if (this.type == "email") {
                    return value;
                }
            },
            numberFormatter(value, event){
                if (value.length > 14)
                    return value.substr(0, 14)
                var cleaned = ('' + value).replace(/\D/g, '')
                var match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
                if (match) {
                    return '(' + match[1] + ') ' + match[2] + '-' + match[3];
                }
                return cleaned
            },
            getNewState(spinnerOpt) {
                // TODO: change this function to make a axios request to the server
                var inputType = this.type;
                var notifValue = this.localData.text;
                if(inputType === "text"){
                    inputType = "sms_number";
                    notifValue = ('' + notifValue).replace(/\D/g, '')
                    if (notifValue != "")
                        notifValue = "+1" + notifValue;
                }
                var data = new FormData();
                //data.set('id', this._uid);
                data.set(inputType, notifValue);
                var csrftoken = Cookies.get('csrftoken');
                var headers = {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                }
                spinnerOpt.state = true
                axios.patch("/subscription/1/", data, {"headers" : headers})
                    .then(response => {
                        console.log("this is after the patch request")
                        console.log(response);
                        this.requestUpdate()
                    
                        spinnerOpt.state = false
                        if (this.newData) {
                            this.newData = false
                        }
                        this.updateMode = false
                    })
                    .catch(console.log);
                console.log(this.localData.text)
            },
            deleteData(spinnerOpt) {
                this.localData.text = ""
                this.getNewState(spinnerOpt)
            },
            cancelUpdate(event, spinnerOpt) {
                spinnerOpt.state = true;
                if (this.serverData.text == '')
                    this.isOpen = false
                else if (this.updateMode)
                    this.updateMode = false
                else if (!this.serverData.verified) {
                    // TODO: Cancel this event by sending a patch request to the api
                    this.deleteData(spinnerOpt);
                    
                }
            }
        },
        watch: {
            serverData(newVal, oldVal) {
                this.localData.text = newVal.text   //this is inputting sms with +1
                this.localData.verified = newVal.verified
            }
        },
        computed: {
        },
        beforeMount() {
            this.localData.text = this.serverData.text   //inputting sms with +1
            this.localData.verified = this.serverData.verified
            this.isOpen = this.visible
        },
    }
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
    .notif-option-card.notif-option-card {
        border-radius: 0;
        border: unset;
        border-top: 1px solid #9B9B9B;
        border-bottom: 1px solid #9B9B9B;
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
</style>
