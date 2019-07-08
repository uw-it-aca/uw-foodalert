<template>
    <generic-page>
        <template #heading>
            You need a Temporary Food Service Permit
        </template>
        <template #body>
         <p>Based on what you’ve told us about your food, you’ll need to obtain a Temporary Food Service Permit to share via Hungry Husky.</p>
          <p>The only food you can share without a permit is either:</p>
          <ul class="ml-4">
            <li>Non-perishable</li>
            <li>Commercially pre-packaged</li>
            <li>Prepared by UW Housing and Food Services or Bay Laurel Catering</li>
          </ul>

          <p>Keep in mind for future events, it takes two weeks to get a permit and a new permit is required for every event. If you have questions about how to share food with Hungry Husky, please email <a href="mailto:hungryhusky@uw.edu">hungryhusky@uw.edu</a>.</p>
        </template>
        <template #navigation>
            <div class="mt-5">
            <b-row align-h="between">
              <b-col md="4" lg="3" order-md="2"><b-button href="https://www.ehs.washington.edu/workplace/food-safety-program/temporary-food-service-permit" class="mb-3" type="submit" block variant="primary">Get a permit</b-button>
              </b-col>
              <b-col md="4" lg="3" order-md="1"></b-col>
            </b-row>
          </div>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
    import GenericPage from "../../components/generic-page.vue";
    export default {
        components:{
            "generic-page": GenericPage,
        },
    }
</script>