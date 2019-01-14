<template>
    <div class="">
        <b-container class="pt-3">
            <h1 class="h4">{{ headerText }}</h1>
        </b-container>
        <hr>
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
                case '/ended':
                    this.headerText = 'Your Notification Was Sent'
                    break;
                case '/update':
                    this.headerText = 'Update An Existing Notification'
                    break;
                case '/signup':
                    this.headerText = 'Sign-up To Receive Notifications'
                    break;
                case '/audit':
                    this.headerText = 'Audit Logs'
                    break;
                default:
                    this.headerText = '';
            }
        }
    }
}
</script>
