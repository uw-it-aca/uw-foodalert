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
  mounted() {
    this.$children[0].$children[0].$data.showUpdateOverlay = true;
    const headers = {
      'Content-Type': 'application/json',
    };

    axios.get('/api/v1/subscription/?netID=' + this.netID, {headers})
        .then((result) => {
          if (result.data.length) {
            this.$router.push({
              name: 's-notifications',
              params: {agree: true,}
            });
          } else {
            this.$children[0].$children[0].$data.showUpdateOverlay = false;
          }
        }).catch((error) => this.showErrorPage(error.response, 's-welcome'));
  },
};
</script>

<style lang="scss">
</style>
