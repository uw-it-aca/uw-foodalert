<template>
    <b-container class="px-4 pt-3">
    <b-row class="justify-content-center">
        <b-col md="8">
            <p>Select all that apply to your food.</p>
            <b-form-group>
                <form-checkbox-with-tooltip
                 modelt="selected"
                 keyt="non-perishable"
                 valuet="non-perishable"
                 :disabledt="selected.includes('none') || selected.includes('home')">
                    <template #checkbox-text>
                        My food is non-perishable.
                    </template>
                    <template #tooltip-link-text>
                        Examples
                    </template>
                    <template #tooltip-text>
                        Candy, beverages (pasteruized, canned, or bottled), chips, dips.
                    </template>
                </form-checkbox-with-tooltip>
                <form-checkbox-with-tooltip
                 modelt="selected"
                 keyt="pre-packaged"
                 valuet="pre-packaged"
                 :disabledt="selected.includes('none') || selected.includes('home')">
                    <template #checkbox-text>
                        My food was commercially pre-packaged.
                    </template>
                    <template #tooltip-link-text>
                        Examples
                    </template>
                    <template #tooltip-text>
                        Wrapped or boxed baked goods (cakes, pies), chips, store-bought ice cream.
                    </template>
                </form-checkbox-with-tooltip>
                <b-form-checkbox
                 v-model="selected"
                 key="home"
                 value="home"
                 :disabled="selected.includes('non-perishable') || selected.includes('pre-packaged') || selected.includes('none')"
                >{{"My food was prepared at home."}}</b-form-checkbox>
                <b-form-checkbox
                 v-model="selected"
                 key="none"
                 value="none"
                 :disabled="selected.includes('non-perishable') || selected.includes('pre-packaged') || selected.includes('home')"
                >{{"None of the above."}}</b-form-checkbox>
            </b-form-group>

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