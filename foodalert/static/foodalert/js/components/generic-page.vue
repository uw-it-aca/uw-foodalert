<template>
    <div class="page">
        <b-collapse id="notif-container" :visible="notificationState">
            <slot name="notification"></slot>
        </b-collapse>
        <div class="page-content">
            <slot name="heading"></slot>
            <slot name="body"></slot>
            <slot name="navigation"></slot>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        startWithNotification: {
            type: Boolean,
            default: false
        },
        timeoutOfNotification: {
            type: Number,
            default: 5
        },
    },
    data() {
        return {
            notificationState: false,
        }
    },
    beforeMount() {
        if(startWithNotification) {
            this.notificationState = true;
        }
    },
    beforeRouteUpdate(to, from, next) {
        this.getHeader(to);
        next();
    },
    beforeRouteEnter(to, from, next) {
        next(function(vm) { vm.getHeader(to) });
    },
    methods: {
        getHeader(to) {
            switch (to.path) {
                case '/':
                    this.headerText = 'Create Food Notification';
                    break;
                case '/ended/':
                case '/ended':
                    this.headerText = 'Your Notification Was Sent'
                    break;
                case '/update/':
                case '/update':
                    this.headerText = 'Update An Existing Notification'
                    break;
                case '/signup/':
                case '/signup':
                    this.headerText = 'Sign-up To Receive Notifications'
                    break;
                case '/audit/':
                case '/audit':
                    this.headerText = 'Audit Logs'
                    break;
                case '/subscribed/':
                case '/subscribed':
                    this.headerText = 'You Signed Up For Food Notifications!'
                    break;
                case '/categories/':
                case '/categories':
                    this.headerText = 'Tell us about your food'
                    break;
                default:
                    this.headerText = '';
            }
        }
    }
}
</script>