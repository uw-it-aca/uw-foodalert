<template>
<div>
  <welcome-page #banner>
  </welcome-page>
</div>
</template>

<script type="text/javascript">
import CustomTextBox from '../components/custom-text-box.vue';
import WelcomePage from '../components/welcome-page.vue';
  export default {
    components: {
      "custom-text-box": CustomTextBox,
      "welcome-page": WelcomePage,
    },

    data() {
      return {
      }
    }
  }
</script>

<style lang="scss">
</style>
