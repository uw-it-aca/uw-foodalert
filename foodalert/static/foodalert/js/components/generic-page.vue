<template>
    <div class="page">
        <b-collapse id="notif-container" v-model="notificationState">
            <slot name="notification"></slot>
        </b-collapse>
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

<style media="screen">
  #standard-heading {
    font-size: 2rem;
    line-height: 1.2;
    font-weight: 600;
    letter-spacing: .004rem;
  }
  #standard-body {
    font-size:1.14rem;
    line-height: 1.5;
    font-weight: 400;
    letter-spacing: .012rem;
    color: #333;
  }


</style>
