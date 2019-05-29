<template>
    <b-container class="px-4 pt-3">
    <b-row class="justify-content-center">
        <b-col md="8">
            <p>Select all that apply to your food.</p>
            <b-form-group>
              <b-form-checkbox-group
                id="checkbox-group-1"
                v-model="selected"
                :options="options"
                name="flavour-1"
                stacked
              ></b-form-checkbox-group>
            </b-form-group>

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
        </b-col>
    </b-row>
    </b-container>
</template>

<script type="text/javascript">
  export default {
    data() {
      return {
        selected: [], // Must be an array reference!
        options: [
          { text: 'Orange', value: 'orange' },
          { text: 'Apple', value: 'apple' },
          { text: 'Pineapple', value: 'pineapple' },
          { text: 'Grape', value: 'grape' }
        ]
      }
    }
  }
</script>
