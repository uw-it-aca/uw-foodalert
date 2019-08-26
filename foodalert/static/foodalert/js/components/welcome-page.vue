<template>
    <generic-page>
      <template #banner>
          <div style="border-bottom: 1px solid #ebebeb;">
            <b-navbar class="mx-auto" style="height: 64px; max-width: 1232px;">
              <b-navbar-brand class="pl-2" href="#">
                <img :src="require('../../img/food-alert-logo.svg')"
                       alt="UW Food Alert Logo" height="24" class="d-none d-sm-none d-md-block">
                <img :src="require('../../img/uw-logo.svg')"
                              alt="UW Logo" height="24" class="d-block d-sm-block d-md-none">
              </b-navbar-brand>
              <b-navbar-nav class="ml-auto">
                <p class="my-auto" style="font-size: 14px; font-weight: 400; color: #484848; -moz-osx-font-smoothing: grayscale;
    ">UW NetID</p>
                <b-button variant="link" style="font-size: 14px; font-weight: 300;" type="submit">Sign out</b-button>
              </b-navbar-nav>
            </b-navbar>
          </div>
      </template>
      <template #heading>
        Welcome
      </template>
      <template #body>
        <slot name="paragraph"></slot>
      </template>
      <template #navigation>
        <div class="mt-5">
          <b-row align-h="end">
            <b-col md="3" lg="3">
              <b-button class="mb-3 button-text" type="submit" block variant="primary"
                        size="lg" style="white-space: nowrap;"
                        @click="getNextPage()">
                          Let's go
              </b-button>
            </b-col>
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
