<template>
    <div class="page">
        <div id="standard-notification">
            <b-collapse id="notif-container" v-model="notificationState">
                <b-container fluid class="text-center py-3" :style="notifStyle">
                    <b-container>
                        <b-row class="justify-content-center">
                            <b-col md="8">
                                <div class="h5 text-white pt-2">
                                  <slot name="notification"></slot>
                                </div>
                            </b-col>
                        </b-row>
                    </b-container>
                </b-container>
            </b-collapse>
        </div>
        <div class="page-content pb-2">
            <slot name="banner"></slot>
            <b-container>
              <b-row class="justify-content-center">
                <b-col md="8" class="page-content-padding">
                  <h1 id="standard-heading" class="pt-4 pb-2"><slot name="heading"></slot></h1>
                  <div id="standard-body"><slot name="body"></slot></div>
                  <slot name="navigation"></slot>
                </b-col>
              </b-row>
            </b-container>
        </div>
        <footer id="relative-footer" class="text-center">
          <a href="mailto:help@uw.edu?subject=Hungry Husky support">Contact support</a>
          <p>© 2019 University of Washington</p>
        </footer>
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
            default: "#0070C9"
        }
    },
    data() {
        return {
            notificationState: false,
            notifStyle: "",
        }
    },
    methods: {
        showNotification: function() {
            setTimeout(() => {this.notificationState = true;}, 250);
            setTimeout(() => {this.notificationState = false;}, this.timeoutOfNotification);
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
        line-height: 1.125em;
        font-weight: 600;
        color: #484848;
    }
    #standard-body {
        font-size:16px;
        line-height: 1.375;
        font-weight: 400;
        color: #484848;
    }

    .page .page-content .page-content-padding {
      padding-left: 24px;
      padding-right: 24px;
      padding-bottom: 8px;
    }

    .page {
        display: flex;
        min-height: 100vh;
        flex-direction: column;
        align-content: space-between;
    }

    #relative-footer {
        margin-top: auto;
        font-size: 12px;
        width: 100%;
    }
</style>
