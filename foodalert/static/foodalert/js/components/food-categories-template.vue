<template>
    <b-container class="px-4 pt-3">
    <b-row class="justify-content-center">
        <b-col md="8">
            <p>Select all that apply to your food.</p>
            <b-form-group>
              <b-form-checkbox
                v-model="selected"
                key="non-perishable"
                value="non-perishable"
                :disabled="selected.includes('none') || selected.includes('home')"
              >{{"My food is non-perishable. "}}<a href="#" @click.prevent.stop="tooltip1 = !tooltip1">Examples</a></b-form-checkbox>
              <div class="tooltip-example" v-if="tooltip1">Candy, beverages (pasteruized, canned, or bottled), chips, dips.</div>
              <b-form-checkbox
                v-model="selected"
                key="pre-packaged"
                value="pre-packaged"
                :disabled="selected.includes('none') || selected.includes('home')"
              >{{"My food was commercially pre-packaged. "}}<a href="#" @click.prevent.stop="tooltip2 = !tooltip2">Examples</a></b-form-checkbox>
              <div class="tooltip-example" v-if="tooltip2"> Wrapped or boxed baked goods (cakes, pies), chips, store-bought ice cream.</div>
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
        tooltip1: false,
        tooltip2: false,
      }
    }
  }
</script>

<style>
    .custom-control-label::before, .custom-control-label::after {
        transform: scale(1.5);
        padding: 10px;
    }

    .custom-control-label {
        padding-left: 1rem;
        padding-bottom: 1.5rem;
        padding-top: 0.3rem;
    }

    .tooltip-example {
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #e9e9e9;
        color: #707070;
    }
</style>
