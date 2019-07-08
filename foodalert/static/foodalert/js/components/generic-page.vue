<template>
    <div class="page">
        <div id="standard-notification">
            <b-collapse id="notif-container" v-model="notificationState">
                <b-container fluid class="py-3" :style="notifStyle">
                    <b-container>
                        <b-row class="justify-content-center">
                            <b-col md="8">
                                <h2 style="color: white;">
                                    <strong>
                                        <slot name="notification"></slot>
                                    </strong>
                                </h2>
                            </b-col>
                        </b-row>
                    </b-container>
                </b-container>
            </b-collapse>
        </div>
        <div class="page-content">
            <slot name="banner"></slot>
            <b-container>
              <b-row class="justify-content-center">
                <b-col md="8">
                  <h1 id="standard-heading" class="pt-4 pb-2"><slot name="heading"></slot></h1>
                  <div id="standard-body"><slot name="body"></slot></div>
                  <slot name="navigation"></slot>
                </b-col>
              </b-row>
            </b-container>
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
            default: 3000
        },
        notificationColor: {
            type: String,
            default: "#1DA83F"
        }
    },
    data() {
        return {
            notificationState: false,
            notifStyle: "",
        }
    },
    methods: {
        showNotification: async function() {
            await setTimeout(() => {this.notificationState = true;}, 250);
            await setTimeout(() => {this.notificationState = false;}, this.timeoutOfNotification + 250);
        }
    },
    beforeMount() {
        if(this.startWithNotification) {
            this.showNotification();
        }
        this.notifStyle = "background-color: " + this.notificationColor + ";";
    },
}
</script>

<style>
    #standard-notification {
        height: 0;
        overflow: visible;
        position: relative;
        z-index: 1;
    }
    #standard-heading {
        font-size: 32px;
        line-height: 1.2;
        font-weight: 600;
        letter-spacing: .004rem;
        color: #484848;
    }
    #standard-body {
        font-size:16px;
        line-height: 1.5;
        font-weight: 400;
        color: #484848;
    }
</style>
