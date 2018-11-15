<template>
    <div class="">
        <b-container class="pt-3">
            <h1 class="h4"> TEST TEXT</h1>
        </b-container>
        <hr>
        <router-view>

        </router-view>
    </div>
</template>

<script>
export default {
    props: {
        headerText: {
            type: String,
            //required: true,
        }
    },
    data() {
        return {
            headerText: '',
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
