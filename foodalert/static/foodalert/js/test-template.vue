<template>
<div>
  <b-container>
    <b-row class="justify-content-center">
      <b-col md="8">
        <h1 class="pt-4">Test</h1>
        <p>
          This is a test.
        </p>
        <custom-text-box>

        </custom-text-box>
      </b-col>
    </b-row>
  </b-container>
</div>
</template>

<script type="text/javascript">
import CustomTextBox from './components/custom-text-box.vue';
  export default {
    components: {
      "custom-text-box": CustomTextBox,
    },

    data() {
      return {
      }
    }
  }
</script>

<style lang="scss">
</style>
