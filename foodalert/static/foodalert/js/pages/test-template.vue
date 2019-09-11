<template>
  <div>
    <b-navbar class="mx-auto" style="height: 64px;">
      <b-navbar-brand class="pl-2 pb-2">
        <img :src="require('../../img/food-alert-logo.svg')"
              alt="UW Food Alert Logo" height="22"
              >
      </b-navbar-brand>
    </b-navbar>
    <audit-template></audit-template>
  </div>
</template>

<script type="text/javascript">
import AuditTemplate from '../components/audit-template.vue';

export default {
  components: {
    'audit-template': AuditTemplate,
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
