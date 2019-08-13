<template>
<div>
  <welcome-page nextPageName="h-food-service">
    <template #paragraph>
      <p>Hungry Husky lets you share your leftover event food with those who
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
  beforeMount() {
    axios.get('/notification/?host_netid=' + this.netID).then((result) => {
      result.data = result.data.filter((d)=>!d.ended);
      if (result.data.length) {
        this.$router.push({name: 'h-update', params: {
          notificationText: 'You already have an event running.',
        }});
      }
    }).catch((error) => this.showErrorPage(error.response, 'h-welcome'));
  },
};
</script>
