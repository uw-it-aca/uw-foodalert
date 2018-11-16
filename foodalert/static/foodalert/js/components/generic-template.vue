<template>
    <div class="">
        <b-container class="pt-3">
            <h1 class="h4">{{ headerText }}</h1>
        </b-container>
        <hr>
        <router-view>

        </router-view>
    </div>
</template>

<script>
export default {
    data() {
        return {
            headerText: 'TEST TEXT',
        }
    },
    beforeRouteUpdate(to, from, next) {
        switch (to) {
            case '/':
                this.headerText = 'Create Food Notification';
                break;
            case '/ended':
                this.headerText = 'Your Notification was Sent'
            default:
                this.headerText = '';

        }
    }
}
</script>
