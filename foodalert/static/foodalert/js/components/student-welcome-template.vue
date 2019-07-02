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
          With Hungry Husky, you’ll receive notifications through email, text, or both whenever events on campus have available food.
        </p>
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
