<template>
  <b-container>
    <h1>Tell us about your event</h1>
    <b-form @submit="proceed">
      <label class="mt-4" for="eventName">Event name</label>
      <b-form-input type="text" placeholder="FIUTS weekly club meeting" id="eventName"></b-form-input>
      <b-form-group
        class="mt-4"
        label="Do you have a UW Temporary Food Service Permit? What is this?"
        v-model="this.selected"
      >
        <b-form-radio value="Yes" name="yesNo">Yes</b-form-radio>
        <br>
        <b-form-radio value="No" name="yesNo">No</b-form-radio>
      </b-form-group>
      <div class="mt-5">
        <b-row align-h="between">
          <b-col md="4" lg="2" order-md="2">
            <b-button class="mb-3" type="submit" block variant="primary">Continue</b-button>
          </b-col>
          <b-col md="4" lg="2" order-md="1">
            <b-button type="submit" block variant="light">Back</b-button>
          </b-col>
        </b-row>
      </div>
    </b-form>
  </b-container>
</template>

<script>
import LabelledInput from "./labelled-input.vue";

export default {
  data() {
    return {
      selected: ""
    };
  },
  methods: {
    updateValue(context) {
      this.$emit("updateState", context);
    },
    setValue(context, value) {
      this.$emit("setState", context, value);
    },
    proceed() {
      this.$router.push({ name: "form" });
    }
  },
  components: {
    "labelled-input": LabelledInput
  }
};
</script>


<style lang="css" scoped>
</style>
