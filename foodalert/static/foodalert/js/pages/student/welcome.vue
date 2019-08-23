<template>
<div>
  <welcome-page nextPageName="s-responsibilities">
    <template #paragraph>
      <p>When you sign up with UW Food Alert, you’ll receive notifications
        through email, text, or both whenever events on campus
        have available food.</p>
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
    axios.get('/subscription/?netID=' + this.netID)
      .then((result) => {
        if (result.data.length) {
          this.$router.push({name: 's-notifications'});
        }
    }).catch((error) => this.showErrorPage(error.response, 's-welcome'));
  },
};
</script>

<style lang="scss">
</style>
