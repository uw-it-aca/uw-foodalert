<template>
<div>
  <welcome-page nextPageName="h-food-service">
    <template #paragraph>
      <p>UW Food Alert lets you share your leftover event food with those who
        need it most in the UW community. With your help, we can help reduce
        food insecurity among students and others—and reduce food waste at
        the same time.</p>
      <p>We’ll guide you through all the steps needed to share your food
        safely and responsibly.</p>
    </template>
  </welcome-page>
</div>
</template>

<script type="text/javascript">
import WelcomePage from '../../components/welcome-page.vue';
const axios = require('axios');

export default {
  components: {
    'welcome-page': WelcomePage,
  },
  data() {
    return {
    };
  },
  mounted() {
    // first child is welcome-page
    // second child is generic-page
    this.$children[0].$children[0].$data.showUpdateOverlay = true;

    const headers = {
      'Content-Type': 'application/json',
    };

    axios.get(
        '/v1/notification/?host_netid=' + this.netID,
        {headers},
    ).then((result) => {
      result.data = result.data.filter((d)=>!d.ended);

      if (result.data.length) {
        this.$router.push({name: 'h-update', params: {
          notificationText: 'You already have an event running.',
        }});
      } else {
        this.$children[0].$children[0].$data.showUpdateOverlay = false;
      }
    }).catch((error) => this.showErrorPage(error.response, 'h-welcome'));
  },
};
</script>
