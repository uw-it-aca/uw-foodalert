<template>
    <generic-page>
        <template #heading>
            Notification preferences
        </template>
        <template #body>
            <p>
                Select how you will like to receive notifications. Please choose at least one.                                                      
            </p>
            <enable-notification :collapse_id="collapse_id">
                <p slot="message">Turn on to receive notifications. Please choose at least one.</p>
            </enable-notification>
            <notification-option 
                accord_id="text" 
                type="phonenumber" 
                label="Enter a new phone number" 
                description="Carrier rates may apply"
                @check-collapse="checkCollapse"
                :collapse_notif.sync="collapse_notif">
                <template #opt_heading>
                    Text 
                </template>
            </notification-option>
            <notification-option 
                accord_id="email" 
                type="email" 
                @check-collapse="checkCollapse"
                :collapse_notif.sync="collapse_notif"
                label="Enter an email">
                <template #opt_heading>
                    Email 
                </template>
            </notification-option>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
    import GenericPage from "../../components/generic-page.vue";
    import EnableNotif from "../../components/enable-notification.vue";
    import NotifOption from "../../components/notification-option.vue";

    export default {
        components:{
            "generic-page": GenericPage,
            "enable-notification": EnableNotif,
            "notification-option": NotifOption,
        },
        props: {
            bid: String,
        },
        data() {
            return {
                collapse_id: "enable-notification",
                collapse_notif: false, 
            }
        },
        methods: {
            checkCollapse(id){
                if(!this.collapse_notif){
                    this.collapse_notif = true;
                }
            }
        },
        watch: {
            collapse_notif(newValue, oldValue) {
                if(newValue){
                    this.$root.$emit('bv::toggle::collapse', this.collapse_id);
                }
            }
        }
    }
</script>