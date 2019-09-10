<template>
  <div>
    <b-navbar class="mx-auto" style="height: 64px;">
      <b-navbar-brand class="pl-2 pb-2">
        <img :src="require('../../img/food-alert-logo.svg')"
              alt="UW Food Alert Logo" height="22"
              >
      </b-navbar-brand>
    </b-navbar>
    <audit-controller></audit-controller>
  </div>
</template>

<script type="text/javascript">
import AuditController from '../components/audit-controller.vue';

export default {
  components: {
    'audit-controller': AuditController,
  },

  data() {
    return {
    };
  },
  methods: {
  },
};
</script>

<style lang="scss">
</style>
