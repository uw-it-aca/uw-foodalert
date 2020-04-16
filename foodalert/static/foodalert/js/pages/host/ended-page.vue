<template>
  <generic-page startWithNotification>
    <template #notification>
      Your update was sent.
    </template>
    <template #heading>
      Our sincere thanks.
    </template>
    <template #body>
      <p>Thank you for sharing food. Your generosity means that fewer people
         have to worry about food insecurity at UW. You've also contributed
         to decreasing the University's food waste. We really appreciate your
         generosity and thoughtfulness. Please visit UW Food Alert next time
         you have leftover food to share.</p>
    </template>
    <template #navigation>
      <div class="mt-5">
        <b-row align-h="end">
          <b-col md="4">
            <b-button class="mb-3 button-text" type="submit"
                      block variant="primary"
                      size="lg" style="white-space: nowrap;"
                      @click="$router.push({'name': 'h-welcome'})">
                        New notification
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
        `/api/v1/notification/?host_netid=${this.netID}`,
        {headers},
    ).then((result) => {
      result.data = result.data.filter((d) => !d.ended);

      if (result.data.length) {
        this.$router.push({
          name: 'h-update',
          params: {
            notificationText: 'You already have an event running.',
          },
        });
      } else {
        this.$children[0].$data.showUpdateOverlay = false;
      }
    }).catch((error) => this.showErrorPage(error.response, 'h-ended'));
  },
};
</script>
