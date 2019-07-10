<template>
    <generic-page>
        <template #heading>
            Before you receive notifications
        </template>
        <template #body>
            <p>
                We'll need you to agree to the following terms.
            </p>
            <b-form @submit="getNextPage()" ref="resForm">
                <custom-checkbox
                    v-model="selected"
                    name="cond1"
                    value="cond1" required>
                    We cannot confirm all potential allergy ingredients.
                </custom-checkbox>
                <custom-checkbox
                    v-model="selected"
                    name="cond2"
                    value="cond2" required>
                    Placeholder for terms and service
                </custom-checkbox>
                <div class="mt-5">
                    <b-row align-h="between">
                        <b-col md="4" lg="3" order-md="2">
                        <b-button class="mb-3" type="submit" block variant="primary">Continue</b-button>
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
    import GenericPage from "../../components/generic-page.vue";
    import CollapseTextBox from "../../components/collapse-text-box.vue";
    import CustomCheckbox from "../../components/custom-checkbox.vue";

    export default {
        components:{
            "generic-page": GenericPage,
            "collapse-text-box": CollapseTextBox,
            "custom-checkbox": CustomCheckbox,
        },
        props: {
            bid: String,
        },
        methods: {
            getNextPage() {
                this.$router.push({ name: 's-notifications' });
            },
        },
        data() {
            return {
                selected: [],
            }
        }
    }
</script>