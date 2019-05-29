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
            <b-col md="4" lg="3" order-md="2"><b-button class="mb-3" type="submit" block variant="primary">Continue</b-button>
            </b-col>
            <b-col md="4" lg="3" order-md="1"></b-col>
          </b-row>
        </div>
      </b-col>
    </b-row>
  </b-container>

</div>
</template>

=======
  <b-navbar style="background-color: #4b2e83">
    <b-container class="hh-logo">
      <b-navbar-brand href="#">
        <b-img v-bind="mainProps" src="https://s3-us-west-2.amazonaws.com/uw-s3-cdn/wp-content/uploads/sites/98/2014/09/07214416/W-Logo_White.png" alt="UW Block Logo"></b-img>
      </b-navbar-brand>
    </b-container>
  </b-navbar>
  <b-container>
    <b-row class="justify-content-center">
      <b-col md="8">
        <!-- <b-container> -->
          <h1 class="pt-4">Welcome</h1>
            <p>
              Hungry Husky lets you share your leftover event food with those who need it most in the UW community. With your help, we can help reduce food insecurity among students and others—and reduce food waste at the same time.
            </p>
            <p>We’ll guide you through all the steps needed to share your food safely and responsibly.</p>
        <!-- </b-container>
        <b-container> -->
          <div class="mt-5">
             <b-row align-h="between">
               <b-col md="4" lg="3" order-md="2">
                 <b-button class="mb-3" type="submit" block variant="primary">Continue</b-button>
               </b-col>
               <b-col md="4" lg="3" order-md="1">
                 <b-button class="hh-back-button" type="submit" block variant="light">Back</b-button>
               </b-col>
             </b-row>
           </div>
         <!-- </b-container> -->
      </b-col>
    </b-row>
  </b-container>
</div>
</template>

<div class="container">
  <p>Hello darkness my old friend</p>
</div>

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
