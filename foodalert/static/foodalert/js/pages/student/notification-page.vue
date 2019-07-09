<template>
    <generic-page>
        <template #heading>
            Notification preferences
        </template>
        <template #body>
            <p>
                Select how you will like to receive notifications. PLease choose at least one.                                                      
            </p>
            <b-form @submit="getNextPage()" ref="resForm">
                <b-form-checkbox
                    v-model="selected"
                    name="cond1"
                    value="cond1" required>
                    We cannot confirm all potential allergy ingredients.
                </b-form-checkbox>
                <b-form-checkbox
                    v-model="selected"
                    name="cond2"
                    value="cond2" required>
                    Placeholder for terms and service
                </b-form-checkbox>
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

    export default {
        components:{
            "generic-page": GenericPage,
            "collapse-text-box": CollapseTextBox,
        },
        props: {
            bid: String,
        },
        methods: {
            getNextPage() {
                this.$router.push({ name: 's-responsibilities' });
            },
        },
        data() {
            return {
                selected: [],
            }
        }
    }
</script>