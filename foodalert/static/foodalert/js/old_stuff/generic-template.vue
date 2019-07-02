<template>
    <div class="">
        <b-container class="pt-3">
            <h2 class="heading-text"><b>{{ headerText }}</b></h2>
        </b-container>
        <router-view :subId="this.subId">

        </router-view>
    </div>
</template>

<script>
export default {
    props: {
        subId: Number,
    },
    data() {
        return {
            headerText: '',
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

<style>
    .header-text < b {
        font-family: Helvetica;
    }
</style>
