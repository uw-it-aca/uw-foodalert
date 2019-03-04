<template>
  <b-container>
    <h1>Tell us about your event</h1>
    <b-form @submit="proceed">
      <form-category>
        <label for="eventName">
          Event Name
        </label>
        <b-form-input
          type="text" 
          placeholder="FIUTS weekly club meeting"
          id="eventName">
        </b-form-input>
        <b-form-group label="Individual radios" v-model="this.selected">
          <b-form-radio value="Yes" name="yesNo">Yes</b-form-radio>
          <b-form-radio value="No" name="yesNo">No</b-form-radio>
        </b-form-group>
         <b-button type="submit">Submit</b-button>
      </form-category>
    </b-form>
  </b-container>
</template>

<script>
    import FormCategory from './form-category.vue';
    import LabelledInput from './labelled-input.vue';
    import PopupContainer from "./popup-container.vue";

    export default {
        data(){
          return{
            selected: ""
          }
        },
        methods: {
            updateValue(context) {
                this.$emit('updateState',  context);
            },
            setValue(context, value) {
                this.$emit('setState', context, value);
            },
            proceed() {
              this.$router.push({ name: 'form'});
            }
        },
        components: {
            'form-category': FormCategory,
            'labelled-input': LabelledInput,
            'popup-container': PopupContainer,
        }
    }
</script>


<style lang="css" scoped>
</style>
