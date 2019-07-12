<template>
    <generic-page>
        <template #heading>
            Responsibilities
        </template>
        <template #body>
            <p>
                To ensure the safety of the food being shared, we'll need you to agree to the following requirements.
            </p>
            <b-form @submit="getNextPage()" ref="resForm">
                <b-form-checkbox
                    v-model="selected"
                    value="cond1">
                    <span>
                        My office is responsible for the safety of this food.
                        <b-link herf="#" v-b-toggle.cond1-info> Learn More</b-link>
                    </span>
                </b-form-checkbox>
                <collapse-text-box bid="cond1-info">
                    You are responsible for food safety under the approval of the Temporary Food Permit, this same level of responsibility applies when using the Hungry Husky App.
                </collapse-text-box>
                <b-form-checkbox
                    v-model="selected"
                    value="cond2">
                    <span>
                        For potentially hazardous food, it has not been out of heating or cooling for more than <strong>four hours</strong>.
                        <b-link herf="#" v-b-toggle.cond2-info> Learn More</b-link>
                    </span>
                </b-form-checkbox>
                <collapse-text-box bid="cond2-info">
                    Information is missing
                </collapse-text-box>
                <div class="mt-4">
                    <b-row align-h="between">
                        <b-col md="4" lg="3" order-md="2">
                        <b-button class="mb-3" size="lg" type="submit" block variant="primary" :disabled="selected.length != 2">Continue</b-button>
                        </b-col>
                        <b-col md="4" lg="3" order-md="1">
                        <b-button class="hh-back-button" size="lg" type="submit" block variant="outline-secondary" @click="getBackPage()">Back</b-button>
                        </b-col>
                    </b-row>
                </div>
            </b-form>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
    import GenericPage from "../../components/generic-page.vue";
    import CollapseTextBox from "../../components/collapse-text-box.vue";

    export default {
        components:{
            "generic-page": GenericPage,
            "collapse-text-box": CollapseTextBox,
        },
        methods: {
            getNextPage() {
                this.$router.push({ name: 'h-form' });
            },
            getBackPage() {
                this.$router.push({ name: 'h-food-service' });
            }
        },
        data() {
            return {
                selected: [],
            }
        }
    }
</script>
