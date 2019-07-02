<template>
    <div class="page">
        <b-collapse id="notif-container" v-model="notificationState">
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
            default: 5000
        },
    },
    data() {
        return {
            notificationState: false,
        }
    },
    methods: {
        showNotification: async function() {
            this.notificationState = true;
            await setTimeout(() => {this.notificationState = false;}, this.timeoutOfNotification);
        }
    },
    beforeMount() {
        if(this.startWithNotification) {
            this.showNotification();
        }
    },
}
</script>