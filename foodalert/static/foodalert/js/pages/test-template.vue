<template>
  <generic-page startWithNotification :timeoutOfNotification="3000">
    <template #notification>
      Your notification has been sent.
    </template>
    <template #body>
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
  export default {
    components: {
      "generic-page": GenericPage,
      "notification-option": NotificationOption,
    },

    data() {
      return {
      }
    }
  }
</script>

<style lang="scss">
</style>
