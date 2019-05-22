<template>
<div>
  <b-container fluid class="py-2" style="background-color: #4b2e83">
    <b-row class="justify-content-center">
      <b-col md="8">
        <b-img v-bind="mainProps" src="https://s3-us-west-2.amazonaws.com/uw-s3-cdn/wp-content/uploads/sites/98/2014/09/07214416/W-Logo_White.png" alt="UW Block Logo"></b-img>
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
            <b-col md="4" lg="3" order-md="2">
              <b-button class="mb-3" type="submit" block variant="primary">Continue</b-button>
            </b-col>
            <b-col md="4" lg="3" order-md="1">
            </b-col>
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
        mainProps: { width: 40, height: 27 } // UW Block Logo has aspect ratio of 150:101
      }
    }
  }
</script>

<style lang="scss">
    @import '../../css/_mixins.scss';
    .hh-logo {
      outline: 1px solid red;
      // padding-left: 15px !important;
      // padding-right: 15px !important;

      @include breakpoint(tablet) {
       outline-color: #f5f5f5;
       // padding-left: 15px !important;
       // padding-right: 15px !important;
      }
      @include breakpoint(desktop) {
       outline-color: blue;
       // padding-left: 15px !important;
       // padding-right: 15px !important;
      }
    }
    .hh-back-button {
        color: #000000 !important;
        /* fill: #d9d7d6 !important; */
        background-color: #f2f2f2 !important;
    }
</style>
