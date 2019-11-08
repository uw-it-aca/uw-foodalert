<template>
    <generic-page>
        <template #heading>
            You need a Temporary Food Service Permit
        </template>
        <template #body>
         <p>
            Based on what you’ve told us about your food, you’ll need to
            obtain a Temporary Food Service Permit to share via UW Food Alert.
          </p>
          <p>The only food that can be shared without a permit is:</p>
          <ul class="ml-4">
            <li>Non-perishable, or</li>
            <li>Commercially pre-packaged, or</li>
            <li>
              Prepared by UW Housing and Food Services or Bay Laurel Catering
            </li>
          </ul>

          <p>
            Keep in mind for future events, it takes two weeks to get a permit
            and a new permit is required for every event. If you have
            questions about how to share food with UW Food Alert, please email
            <a href="mailto:uwfoodalert@uw.edu">uwfoodalert@uw.edu</a>.
            And thanks for thinking of UW Food Alert!
          </p>
        </template>
        <template #navigation>
            <div class="mt-5">
            <b-row align-h="end">
              <b-col md="3" lg="3">
                <b-button
                  href="https://www.ehs.washington.edu/workplace/food-safety-program/temporary-food-service-permit"
                  class="mb-3 button-text"
                  type="submit"
                  block size="lg"
                  variant="primary">
                    Get a permit
                </b-button>
              </b-col>
            </b-row>
          </div>
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
  mounted() {
    this.$children[0].$data.showUpdateOverlay = true;
    const headers = {
      'Content-Type': 'application/json',
    };

    axios.get(
        '/notification/?host_netid=' + this.netID,
        {headers},
    ).then((result) => {
      result.data = result.data.filter((d)=>!d.ended);

      if (result.data.length) {
        this.$router.push({
          name: 'h-update',
          params: {notificationText: 'You already have an event running.'}});
      } else {
        this.$children[0].$data.showUpdateOverlay = false;
      }
    }).catch((error) => this.showErrorPage(error.response, 'h-need-permit'));
  },
};
</script>
