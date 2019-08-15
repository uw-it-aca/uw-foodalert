<template>
  <generic-page :timeoutOfNotification="3000">
    <template #notification>
      Your notification has been sent.
    </template>
    <template #body>
      <time-picker timeID="randid" startWithCurrent></time-picker>
    </template>
  </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../components/generic-page.vue';
import TimePicker from '../components/time-picker.vue';
export default {
  components: {
    'generic-page': GenericPage,
    'time-picker': TimePicker,
  },

  data() {
    return {
    };
  },
};
</script>

<style lang="scss">
</style>
