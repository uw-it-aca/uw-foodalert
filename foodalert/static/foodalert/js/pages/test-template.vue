<template>
  <generic-page :timeoutOfNotification="3000">
    <template #body>
      <alert-box>
      </alert-box>
      <time-picker timeID="randid" startWithCurrent></time-picker>
      <br/>
      <b-button @click="getNotif">GET Notification</b-button>
    </template>
  </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../components/generic-page.vue';
import TimePicker from '../components/time-picker.vue';
import AlertBox from '../components/alert-box.vue';
const axios = require('axios');
export default {
  components: {
    'generic-page': GenericPage,
    'time-picker': TimePicker,
    'alert-box': AlertBox,
  },

  data() {
    return {
    };
  },
  methods: {
    getNotif() {
      axios.get('/notification/1/')
        .then((response) => {
          console.log(response)
        })
        .catch(console.log)
    }
  }
};
</script>

<style lang="scss">
</style>
