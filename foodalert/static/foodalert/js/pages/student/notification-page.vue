<template>
    <generic-page>
        <template #heading>
            Notification preferences
        </template>
        <template #body>
            <p>
                Select how you will like to receive notifications. Please choose at least one.                                                      
            </p>
            <div class="notification" :disabled="disableNotif" :class="{ 'notif-disabled' : disableNotif }">
                <b-collapse id="enable-notification" v-model="collapse_notif">
                    <b-container @click="checked=(!checked && !disableNotif)">
                        <b-row> 
                            <b-col sm="9" cols="9">
                                <strong>Enable notifications</strong>
                                <p>Turn on to receive notifications. Please choose at least one.</p>
                                <div id="notif-status">
                                    <div v-if=checked class="enabled" > Notifications are enabled</div>
                                    <div v-else class="paused"> Notifications are paused </div>
                                </div>
                            </b-col>
                            
                            <b-col sm="3" cols="3" align-self="center">  
                                <b-form-checkbox 
                                    v-model="checked"
                                    name="enable-switch" 
                                    @click.native.prevent
                                    class="float-right"
                                    :disabled="disableNotif"
                                    switch>
                                </b-form-checkbox> 
                            </b-col>
                        </b-row>
                    </b-container>  
                </b-collapse>
            </div>
            <notification-option 
                accord_id="text" 
                type="text" 
                label="Enter a new phone number" 
                description="Carrier rates may apply"
                :subid="subid"
                :serverData="{ text: notif_info.sms_number, verified: notif_info.number_verified }"
                :requestUpdate="requestUpdate"
                :resendVerif="()=>{return 1}" visible>
                <template #opt_heading>
                    Text 
                </template>
                <template #unverifNotifText="{switchToUpdate}">
                    We sent a text to <b-button variant="link" @click="switchToUpdate" class="px-0">{{notif_info.sms_number}}</b-button>. 
                    Please reply YES to finish signup. <br />
                </template>
            </notification-option>
            <notification-option 
                accord_id="email" 
                type="email" 
                label="Enter an email"
                :subid="subid"
                :serverData="{ text: notif_info.email, verified: notif_info.email_verified }"
                :requestUpdate="requestUpdate"
                :resendVerif="()=>{return 1}">
                <template #opt_heading>
                    Email 
                </template>
                <template #unverifNotifText="{switchToUpdate}">
                    We sent a verification email to <b-button variant="link" @click="switchToUpdate" class="px-0">{{notif_info.email}}</b-button>. <br />
                    Check your spam folder if you don't receive our email. <br />
                </template>
            </notification-option>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
    import GenericPage from "../../components/generic-page.vue";
    import NotifOption from "../../components/notification-option.vue";
    const axios = require('axios');

    export default {
        components:{
            "generic-page": GenericPage,
            "notification-option": NotifOption,
        },
        props: {
            bid: String,
        },
        data() {
            return {
                collapse_notif: false,
                notif_info: {
                    email: "",
                    email_verified: false,
                    sms_number: "",
                    number_verified: false,
                    notif_on: "",
                }, 
                checked: false,
                disableNotif: false,
                subid: undefined,
            }
        },
        methods: {
            getSubID(response) {
                if (response.data[0]){
                    console.log(response.data[0].id);
                    this.subid = response.data[0].id;
                }
                return this.subid;
            },
            formatSms(data){
                // strips sms of the +1
                if(data["sms_number"]){
                    var num = data["sms_number"];
                    num = num.replace("+1", "");
                    data["sms_number"] = num;
                }
                return data;
            },
            requestUpdate() {
                axios.get('/subscription/?netID=' + this.netID)
                    .then(this.getSubID)
                    .then(data => {
                        if(this.subid){
                            var url = "/subscription/" + this.subid + "/";
                            axios.get(url)
                                .then((response) => {
                                    response.data = this.formatSms(response.data)
                                    this.notif_info = response.data;
                                    
                                    // Control the b-collapse
                                    if (this.notif_info.sms_number != '' || this.notif_info.email != '') {
                                        this.collapse_notif = true
                                        if (this.notif_info.email_verified || this.notif_info.number_verified)
                                            this.disableNotif = false
                                        else
                                            this.disableNotif = true
                                    }
                                    else
                                        this.collapse_notif = false
                                })
                                .catch((error) => {
                                        alert("There was an error processing the request");
                                        console.log(error)
                                    });
                        }
                    })
                    .catch((error) => {
                            alert("There was a n error processing the requestS")
                            console.log(error)
                        });
            },
        },
        beforeMount() {
            this.requestUpdate();
        },
    }
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
