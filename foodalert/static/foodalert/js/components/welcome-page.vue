<template>
    <generic-page>
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
              <b-button class="mb-3 button-text" type="submit"
                        block variant="primary"
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
