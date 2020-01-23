<template>
  <generic-page>
    <template #heading>
      Before you receive notifications
    </template>
    <template #body>
      <p>
        We ask that you agree to the following terms of service.
      </p>
      <b-form-group ref="resForm">
        <b-form-checkbox
          v-model="selected"
          id="cond1"
          class="mt-2"
          value="cond1"
          aria-describedby="condition-feedback"
          :state="inputValid('cond1')"
          @change="addToValidate('cond1')">
          <span>
            <span>
              We cannot confirm all potential allergy ingredients.
            </span>
          </span>
        </b-form-checkbox>
        <b-form-checkbox
          v-model="selected"
          id="cond2"
          class="mt-2"
          value="cond2"
          aria-describedby="condition-feedback"
          :state="inputValid('cond2')"
          @change="addToValidate('cond2')">
          <span>
            <span>
              Placeholder for terms and service
            </span>
          </span>
        </b-form-checkbox>
        <div class="invalid-feedback pt-2"
              :class="{'super-show': (inputValid('cond1') == false)
                || (inputValid('cond2') == false)}"
              id="condition-feedback"
              role="alert">
          In order to use the service please agree to above
          responsibilities.
        </div>
        <div class="mt-5">
            <b-row align-h="between">
                <b-col md="3" lg="3" order-md="2">
                  <b-button
                    class="mb-3 button-text"
                    size="lg"
                    type="submit"
                    block variant="primary"
                    aria-label="Agree to the selected checkboxes"
                    @click="getNextPage()">
                      Agree
                  </b-button>
                </b-col>
                <b-col md="3" lg="3" order-md="1">
                </b-col>
            </b-row>
        </div>
      </b-form-group>
    </template>
  </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../../components/generic-page.vue';

export default {
  components: {
    'generic-page': GenericPage,
  },
  props: {
    bid: String,
  },
  methods: {
    getNextPage() {
      this.enableValidation = ['cond1', 'cond2'];

      if (this.selected.length !== 2) {
        return;
      }

      this.$router.push({
        name: 's-notifications',
        params: {agree: true},
      });
    },
    inputValid(fieldValue) {
      if (this.enableValidation.indexOf(fieldValue) !== -1) {
        return (this.selected.indexOf(fieldValue) !== -1 ? null : false);
      }

      return null;
    },
    addToValidate(fieldValue) {
      if (this.enableValidation.indexOf(fieldValue) === -1) {
        this.enableValidation.push(fieldValue);
      }
    },
  },
  data() {
    return {
      selected: [],
      enableValidation: [],
    };
  },
};
</script>
