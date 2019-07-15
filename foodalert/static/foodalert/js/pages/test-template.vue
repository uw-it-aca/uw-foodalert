<template>
  <generic-page>
    <template #body>
      <!--enable-notification>
      </enable-notification!-->
      <notification-option accord_id="abcd1">
        Hello 1
      </notification-option>
      <notification-option accord_id="abcd2">
        Hello 2
      </notification-option>
      <notification-option accord_id="abcd3">
        Hello 3
      </notification-option>
    </template>
  </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../components/generic-page.vue';
import NotificationOption from '../components/notification-option.vue';
import EnableNotification from '../components/enable-notification.vue';
  export default {
    components: {
      "generic-page": GenericPage,
      "notification-option": NotificationOption,
      "enable-notification": EnableNotification,
    },

    data() {
      return {
      }
    }
  }
</script>

<style lang="scss">
</style>
