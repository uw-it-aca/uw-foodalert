
<template>
  <b-container>
    <h1>Responsibilities</h1>
    <b-form @submit="proceed">
      <p></p>

      <b-form-group
        class="mt-4"
        label="To ensure the safety of food being shared, we’ll need you to agree to the following requirements."
      >
        <b-form-checkbox-group id="checkboxes" name="responsibilities" v-model="this.selected">
          <b-form-checkbox value="1">My office is responsible for the safety of this food.</b-form-checkbox>
          <b-form-checkbox value="2">
            For potentially hazardous food, it has not been out of heating or cooling for more than
            <strong>4 hours</strong>.
            <a
              href="#"
              v-b-popover="'There will be content here about why it matters that food is not homemade.'"
              title="Homemade food"
              placement="bottom"
            >Learn more</a>
          </b-form-checkbox>
          <b-form-checkbox value="3">
            The food is not homemade.
            <a
              href="#"
              v-b-popover="'There will be content here about why it matters that food is not homemade.'"
              title="Homemade food"
              placement="bottom"
            >Learn more</a>
          </b-form-checkbox>
        </b-form-checkbox-group>
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