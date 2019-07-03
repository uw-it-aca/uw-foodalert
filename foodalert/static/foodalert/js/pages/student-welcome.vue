<template>
<div>
  <welcome-page>
    <template #paragraph>
      <p>With Hungry Husky, you’ll receive notifications through email, text, or both whenever events on campus have available food.</p>
    </template>
  </welcome-page>
</div>
</template>

<script type="text/javascript">
import WelcomePage from '../components/welcome-page.vue';
  export default {
    components: {
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
