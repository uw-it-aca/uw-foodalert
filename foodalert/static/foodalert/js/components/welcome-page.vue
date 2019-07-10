<template>
    <generic-page>
      <template #banner>
        <b-container fluid class="pt-2" style="background-color: #4b2e83">
          <b-row class="justify-content-center">
            <b-col md="8">
              <b-img :src="require('../../img/uw-logo.png')" alt="UW Block Logo" width="40" height="27"></b-img>
            </b-col>
          </b-row>
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
            <b-col md="5" lg="4" order-md="2"><b-button class="mb-3" type="submit" block variant="primary" size="lg" style="white-space: nowrap;" @click="getNextPage()">Let's get started</b-button>
            </b-col>
            <b-col md="5" lg="4" order-md="1"></b-col>
          </b-row>
        </div>
      </template>
    </generic-page>
</template>

<script>
import GenericPage from "./generic-page.vue";
export default {
	components: {
		"generic-page": GenericPage,
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
		return {}
	},
}
</script>
