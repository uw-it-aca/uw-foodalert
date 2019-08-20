<template>
  <generic-page :timeoutOfNotification="3000">
    <template #body>
      <alert-box>
      </alert-box>
      <time-picker timeID="randid" startWithCurrent></time-picker>
    </template>
  </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../components/generic-page.vue';
import TimePicker from '../components/time-picker.vue';
import AlertBox from '../components/alert-box.vue';
export default {
  components: {
    'generic-page': GenericPage,
    'time-picker': TimePicker,
    'alert-box': AlertBox,
  },

  data() {
    return {
    };
  },
};
</script>

<style lang="scss">
</style>
