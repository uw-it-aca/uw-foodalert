<template>
<div>
  <notification-option accord_id="abcd1">
    Hello 1
  </notification-option>
  <notification-option accord_id="abcd2">
    Hello 2
  </notification-option>
  <notification-option accord_id="abcd3">
    Hello 3
  </notification-option>
</div>
</template>

<script type="text/javascript">
import NotificationOption from '../components/notification-option.vue';
  export default {
    components: {
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
