<template>
    <generic-page>
      <template #banner>
        <b-container fluid class="pt-4 pl-4 pb-4 d-flex" >

          <b-img class="pr-2" :src="require('../../img/food-alert-logo.svg')"
                 alt="UW Food Alert Logo" height="24">
          </b-img>
        </b-container>
      </template>
      <template #heading>
        Welcome
      </template>
      <template #body>
        <slot name="paragraph"></slot>
      </template>
      <template #navigation>
        <div class="mt-5">
          <b-row align-h="between">
            <b-col md="4" lg="4"  order-md="2">
              <b-button class="mb-3" type="submit" block variant="primary"
                        size="lg" style="white-space: nowrap;"
                        @click="getNextPage()">
                          Let's get started
              </b-button>
            </b-col>
            <b-col md="6" lg="5" order-md="1"></b-col>
          </b-row>
        </div>
      </template>
    </generic-page>
</template>

<script>
import GenericPage from './generic-page.vue';
export default {
  components: {
    'generic-page': GenericPage,
  },
  props: {
    nextPageName: String,
  },
  methods: {
    getNextPage() {
      this.$router.push({name: this.nextPageName});
    },
  },
  data() {
    return {};
  },
};
</script>
