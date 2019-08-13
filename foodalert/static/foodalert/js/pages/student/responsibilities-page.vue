<template>
    <generic-page>
        <template #heading>
            Before you receive notifications
        </template>
        <template #body>
            <p>
                We ask that you agree to the following terms of service.
            </p>
            <b-form @submit="getNextPage()" ref="resForm">
                <b-form-checkbox
                    v-model="selected"
                    name="cond1"
                    value="cond1" required>
                    <span>We cannot confirm all potential allergy ingredients.</span>
                </b-form-checkbox>
                <b-form-checkbox
                    v-model="selected"
                    class="mt-3"
                    name="cond2"
                    value="cond2" required>
                    <span>Placeholder for terms and service</span>
                </b-form-checkbox>
                <div style="margin-top: 32px">
                    <b-row align-h="between">
                        <b-col md="4" lg="3" order-md="2">
                        <b-button size="lg" class="mb-3" type="submit" block variant="primary" :disabled="selected.length != 2">Agree</b-button>
                        </b-col>
                        <b-col md="4" lg="3" order-md="1">
                        </b-col>
                    </b-row>
                </div>
            </b-form>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../../components/generic-page.vue';
import CollapseTextBox from '../../components/collapse-text-box.vue';

export default {
  components: {
    'generic-page': GenericPage,
    'collapse-text-box': CollapseTextBox,
  },
  props: {
    bid: String,
  },
  methods: {
    getNextPage() {
      this.$router.push({name: 's-notifications'});
    },
  },
  data() {
    return {
      selected: [],
    };
  },
};
</script>
