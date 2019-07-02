<template>
<div>
  <b-container fluid class="py-2" style="background-color: #4b2e83">
    <b-row class="justify-content-center">
      <b-col md="8">
        <b-img :src="require('../../img/uw-logo.png')" alt="UW Block Logo" width="40" height="27"></b-img>
      </b-col>
    </b-row>
  </b-container>

  <b-container>
    <b-row class="justify-content-center">
      <b-col md="8">
        <h1 class="pt-4">Welcome</h1>
        <p>
          Hungry Husky lets you share your leftover event food with those who need it most in the UW community. With your help, we can help reduce food insecurity among students and others—and reduce food waste at the same time.
        </p>
        <p>We’ll guide you through all the steps needed to share your food safely and responsibly.</p>
        <div class="mt-5">
          <b-row align-h="between">
            <b-col md="4" lg="3" order-md="2"><b-button class="mb-3" type="submit" block variant="primary">Let's get started</b-button>
            </b-col>
            <b-col md="4" lg="3" order-md="1"></b-col>
          </b-row>
        </div>
      </b-col>
    </b-row>
  </b-container>

</div>
</template>

<script type="text/javascript">
  export default {
    data() {
      return {
      }
    }
  }
</script>

<style lang="scss">
</style>
