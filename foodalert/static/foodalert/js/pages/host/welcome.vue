<template>
<div>
  <welcome-page nextPageName="h-food-service">
    <template #paragraph>
      <p>Hungry Husky lets you share your leftover event food with those who need it most in the UW community. With your help, we can help reduce food insecurity among students and others—and reduce food waste at the same time.</p>
      <p>We’ll guide you through all the steps needed to share your food safely and responsibly.</p>
    </template>
  </welcome-page>
</div>
</template>

<script type="text/javascript">
import WelcomePage from '../../components/welcome-page.vue';
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
