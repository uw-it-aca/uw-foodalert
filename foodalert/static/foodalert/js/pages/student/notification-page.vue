<template>
    <generic-page>
        <template #heading>
            Notification preferences
        </template>
        <template #body>
            <p>
                Select how you will like to receive notifications. Please choose at least one.                                                      
            </p>
            <enable-notification>
                <p slot="message">Turn on to receive notifications. Please choose at least one.</p>
            </enable-notification>
            <notification-option 
                accord_id="text" 
                type="phonenumber" 
                label="Enter a new phone number" 
                description="Carrier rates may apply">
                <template #opt_heading>
                    Text 
                </template>
            </notification-option>
            <notification-option 
                accord_id="email" 
                type="email" 
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
            "collapse-text-box": CollapseTextBox,
            "enable-notification": EnableNotif,
            "notification-option": NotifOption,
        },
        props: {
            bid: String,
        },
        methods: {
            getNextPage() {
                this.$router.push({ name: 's-responsibilities' });
            },
        },
    }
</script>