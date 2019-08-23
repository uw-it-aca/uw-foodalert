<template>
    <generic-page>
        <template #heading>
            Your food cannot be shared with UW Food Alert.
        </template>
        <template #body>
          <p>You indicated that your food is homemade, which makes it
            ineligible to be shared with the public via UW Food Alert.</p>
          <p>You are still able to share it with your colleagues in your
            office. If you have questions about how to share food with UW Food Alert, please email
            <a href="mailto:uwfoodalert@uw.edu">uwfoodalert@uw.edu</a>.
            And thanks for thinking of UW Food Alert!</p>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../../components/generic-page.vue';
const axios = require('axios');

export default {
  components: {
    'generic-page': GenericPage,
  },
  beforeMount() {
    axios.get('/notification/?host_netid=' + this.netID).then((result) => {
      result.data = result.data.filter((d)=>!d.ended);
      if (result.data.length) {
        this.$router.push({
          name: 'h-update',
          params: {notificationText: 'You already have an event running.'}});
      }
    }).catch((error) => this.showErrorPage(error.response, 'h-close'));
  },
};
</script>
