<template>
    <b-container class="px-4 pt-3">
    <b-row class="justify-content-center">
        <b-col md="8">
            <p>Select all that apply to your food.</p>
            <tooltip-checkbox></tooltip-checkbox>
            <div class="mt-5">
               <b-row align-h="between">
                 <b-col md="4" lg="3" order-md="2">
                   <b-button class="mb-3" type="submit" block variant="primary" @click="getNextPage()">Continue</b-button>
                 </b-col>
                 <b-col md="4" lg="3" order-md="1">
                   <b-button class="hh-back-button" type="submit" block variant="light" @click="getBackPage()">Back</b-button>
                 </b-col>
               </b-row>
             </div>
        </b-col>
    </b-row>
    </b-container>
</template>

<script type="text/javascript">
  export default {
    methods: {
        getNextPage() {
            if (this.selected.includes('none') || this.selected.includes('home')) {
                this.$router.push({ name: 'notfound' });
            } else if (this.selected.includes('pre-packaged') || this.selected.includes('non-perishable')) {
                this.$router.push({ name: 'responsibilities' });
            }
        },
        getBackPage() {
            this.$router.push({ name: 'notfound' });
        }
    },
    data() {
      return {
        selected: [],
      }
    }
  }
</script>

<style>
</style>
